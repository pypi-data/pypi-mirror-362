#!/usr/bin/env python3

import threading
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import click

from mhdtools import common


def format_coord(x, y):
	return f"x={x:.3f} y={y:.3f}"


def format_cursor_data(v):
	return f"{v:.4e}"


def worker_load(mhd, ret):
	ret['raw'], ret['origin'], ret['spacing'] = common.load_data(mhd)


class MhdView:
	fig = None
	ax = None
	plan = []
	extent = []
	bg_plan = None
	cmap = None

	raw = None
	spacing = None

	default_axis = 'axial'
	default_depth = 0

	alpha = 1
	threshold = 0
	step = 1

	gmax = 0

	slider_depth = None
	button_select_plan = None
	button_show_peak = None

	colorbar = None

	title = ''
	cbar_title = 'auto'
	normalise = None

	rot = 0
	flip = ''

	def __init__(self, cmap, alpha, threshold):
		self.cmap = cmap
		self.alpha = alpha
		self.threshold = threshold

	def set_normalise(self, mode):
		self.normalise = mode

	def set_defaults(self, axis, depth):
		self.default_axis = axis
		self.default_depth = depth

	def set_title(self, title):
		self.title = title

	def set_cbar_title(self, cbar_title):
		self.cbar_title = cbar_title

	def select_cbar_title(self, auto_title):
		return auto_title if self.cbar_title == 'auto' else self.cbar_title

	def set_step(self, step):
		self.step = step

	def set_rot(self, angle):
		if angle % 90 == 0:
			self.rot = ((angle + 360) % 360) // 90

	def set_flip(self, flip):
		self.flip = flip

	def setup_axis(self):
		self.ax.set_xlabel('(mm)')
		self.ax.set_ylabel('(mm)')

		self.ax.format_coord = format_coord

		self.ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
		self.ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))

	def open(self, mhd_files, background_mhd, operation='', log=False):
		workers = []

		fgs = [{} for mhd in mhd_files]
		for mhd, fg in zip(mhd_files, fgs):
			workers.append(threading.Thread(target=worker_load, args=(mhd, fg)))

		bg = {}
		if background_mhd != '.':
			workers.append(threading.Thread(target=worker_load, args=(background_mhd, bg)))
		else:
			self.alpha = 1

		for worker in workers:
			worker.start()

		self.fig = plt.figure()
		self.ax = self.fig.add_axes([0.05, 0.15, 0.70, 0.70])

		self.setup_axis()

		if self.threshold != 0:
			colours = mpl.colormaps[self.cmap](np.linspace(0, 1, 1000))
			newcolor = np.array([0., 0., 0., 0.])
			colours[:int(self.threshold*10), :] = newcolor
			self.cmap = mpl.colors.ListedColormap(colours)

		if self.cmap != '':
			cmappable = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 100), cmap=self.cmap)
			divider = make_axes_locatable(self.ax)
			cax = divider.append_axes("right", size="5%", pad=.05)
			self.colorbar = self.fig.colorbar(cmappable, cax=cax)
			self.colorbar.ax.set_title('')

		if self.cmap == '':
			self.cmap = 'gray'

		for worker in workers:
			worker.join()

		self.raw, self.origin, self.spacing = None, None, None
		if len(mhd_files) == 1:
			self.raw, self.origin, self.spacing  = fgs[0]['raw'], fgs[0]['origin'], fgs[0]['spacing']
		else:
			self.origin = fgs[0]['origin']
			self.spacing = fgs[0]['spacing']
			if operation == 'sum':
				self.raw = np.array(sum([fg['raw'] for fg in fgs]))
			elif operation == 'subtract':
				self.raw = fgs[0]['raw'] - np.array(sum([fg['raw'] for fg in fgs[1:]]))
			elif operation == 'multiply':
				self.raw = np.array(np.multiply(fgs[0]['raw'], fgs[1]['raw']))
			elif operation == 'divide':
				numerator = fgs[0]['raw']
				denominator = np.array(sum([fg['raw'] for fg in fgs[1:]]))
				self.raw = np.divide(numerator, denominator, out=denominator, where=denominator != 0)

		self.background = bg['raw'] if 'raw' in bg else None

		# post computation
		if log:
			threshold = 0
			min_pos = np.min(np.where(self.raw > threshold, self.raw, np.inf))
			# min_pos could be negative or null…
			clean_data = np.where(self.raw > threshold, self.raw, min_pos)
			self.raw = np.log10(clean_data)

		# color bar
		self.gmin = np.min(self.raw)
		self.gmax = np.max(self.raw)
		if self.colorbar is not None:
			if isinstance(self.normalise, tuple):
				title = self.select_cbar_title(f"% of\n{self.normalise[0]:.2e} to {self.normalise[1]:.2e}")
				self.colorbar.ax.set_title(title)
			elif self.normalise == 'global':
				self.colorbar.ax.set_title(self.select_cbar_title(f"% of\n{self.gmax:.2e}"))

	def view(self):
		self.setup_ui()
		self.slider_depth.on_changed(lambda depth: self.update(depth))
		self.button_select_plan.on_clicked(lambda plan: self.select_plan(plan))
		self.button_show_peak.on_clicked(lambda ev: self.select_plan_peak())
		labels = [label.get_text() for label in self.button_select_plan.labels]
		self.button_select_plan.set_active(labels.index(self.default_axis))
		self.update(self.default_depth)

		self.ax.set_title(self.title)
		plt.show()

	def save(self, output, dpi=300):
		self.ax.set_position([.1, .1, .8, .8])
		self.select_plan(self.default_axis)
		self.update(self.default_depth)
		self.ax.set_title(self.title)
		plt.tight_layout()
		plt.savefig(output, dpi=dpi)

	def setup_ui(self):
		ax_depth = self.fig.add_axes([0.1, 0.0, 0.80, 0.05])
		self.slider_depth = mpl.widgets.Slider(
			ax=ax_depth,
			label='depth',
			valmin=0,
			valmax=self.raw.shape[common.to_plan_index[self.default_axis]]-1,
			valinit=self.default_depth,
			valstep=1
		)

		ax_plan = self.fig.add_axes([.83, .5, .15, .21])
		buttons = ('axial', 'sagittal', 'coronal')
		self.button_select_plan = mpl.widgets.RadioButtons(ax_plan, buttons)

		ax_show_peak = self.fig.add_axes([.83, .3, .15, .1])
		self.button_show_peak = mpl.widgets.Button(ax_show_peak, "show peak")

	def close(self):
		plt.close(self.fig)

	def select_plan(self, axis):
		self.plan = common.raw_plan(self.raw, axis)
		if self.step != 1:
			self.plan = self.plan[:, ::self.step, ::self.step]

		if self.background is not None:
			self.bg_plan = common.raw_plan(self.background, axis)
			if self.step != 1:
				self.bg_plan = self.bg_plan[:, ::self.step, ::self.step]

		lspacing = [x for i, x in enumerate(self.spacing) if i != common.to_plan_index[axis]]
		self.extent = [0, self.plan[0].shape[1] * lspacing[0], 0, self.plan[0].shape[0] * lspacing[1]]

		if self.slider_depth is not None:
			self.slider_depth.valmax = self.plan.shape[0]-1
			self.slider_depth.ax.set_xlim(self.slider_depth.valmin, self.slider_depth.valmax)
			self.slider_depth.set_val(
				self.slider_depth.val if self.slider_depth.val <= self.slider_depth.valmax else self.slider_depth.valmax
			)

	def select_plan_peak(self):
		data = common.raw_plan(self.raw, self.button_select_plan.value_selected)
		data = np.array([np.max(plan) for plan in data])
		peaks = data == np.max(data)

		# rotate between peaks if multiple occurrences
		pos = self.slider_depth.val
		peak_depth = 0
		if pos+1 < len(peaks):
			peak_depth = np.argmax(peaks[pos+1:]) + pos + 1

		if not peaks[peak_depth]:
			peak_depth = np.argmax(peaks)

		self.slider_depth.set_val(peak_depth)

	def update(self, x):
		self.ax.cla()
		self.setup_axis()

		if self.bg_plan is not None:
			bg_slice = self.bg_plan[x]
			if self.rot != 0:
				bg_slice = np.rot90(bg_slice, k=self.rot)
			if 'h' in self.flip:
				bg_slice = np.flip(bg_slice, axis=(1))
			if 'v' in self.flip:
				bg_slice = np.flip(bg_slice, axis=(0))
			self.ax.imshow(bg_slice, cmap='gray', extent=self.extent)

		data = self.plan[x]
		lmin = np.min(data)
		lmax = np.max(data)

		if self.rot != 0:
			data = np.rot90(data, k=self.rot)
		if 'h' in self.flip:
			data = np.flip(data, axis=(1))
		if 'v' in self.flip:
			data = np.flip(data, axis=(0))

		norm = None
		if isinstance(self.normalise, tuple):
			norm = mpl.colors.Normalize(self.normalise[0], self.normalise[1])
		elif self.normalise == 'global':
			norm = mpl.colors.Normalize(self.gmin, self.gmax)
		elif self.normalise == 'slice':
			norm = mpl.colors.Normalize(lmin, lmax)

		img = self.ax.imshow(data, norm=norm, cmap=self.cmap, extent=self.extent, alpha=self.alpha)
		img.format_cursor_data = format_cursor_data

		if self.colorbar is not None:
			if self.normalise == 'slice':
				self.colorbar.ax.set_title(self.select_cbar_title(f"% of {lmax:.2e}"))
			elif self.normalise is None:
				cmappable = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, lmax), cmap=self.cmap)
				self.colorbar.update_normal(cmappable)


@click.command()
@click.option(
	'-b', '--background', 'background_mhd', type=click.Path(exists=True), default='.',
	help='background mhd file'
)
@click.option('-a', '--alpha', default=.7, help='foreground alpha if background set')
@click.option('-c', '--cmap', default='', is_flag=False, flag_value='jet', help='foreground colormap')
@click.option('-x', '--axis', 'default_axis', type=click.Choice(common.plans), default='axial', help='default axis')
@click.option('-d', '--depth', 'default_depth', type=int, default=0, help='default depth')
@click.option('-N', '--lnormalise', default=False, is_flag=True, help='normalise foreground data for current layer')
@click.option('-n', '--normalise', default=False, is_flag=True, help='normalise foreground data')
@click.option('-l', '--log', default=False, is_flag=True, help='log scale')
@click.option(
	'-C', '--clamp', type=(float, float), default=None,
	help='clamp data'
)
@click.option('-r', '--rotate', type=int, default=0, help='rotation angle in degrees (multiple of 90)')
@click.option('--flip', type=click.Choice(['', 'h', 'v', 'hv', 'vh']), default='', help='flip horizontally or/and vertically')
@click.option('-t', '--threshold', type=int, default=0, help='threshold (%) for colormap')
@click.option('-D', 'step', type=int, default=1, help='resolution stepping')
@click.option(
	'-O', '--operation', type=click.Choice(('', 'multiply', 'sum', 'subtract', 'divide')), default='',
	help='operation to apply on the data'
)
@click.option('-o', '--output', type=click.Path(), default='', help='output file')
@click.option('-T', '--title', type=str, default='auto', help='figure title')
@click.option('--cbar-title', type=str, default='auto', help='colorbar title')
@click.argument('mhd_files', nargs=-1, type=click.Path(exists=True))
def main(
	mhd_files: str, background_mhd: str, alpha: float, cmap: str, default_axis: str, default_depth: int,
	clamp: float, lnormalise: bool, normalise: bool, log: bool, threshold: int, step: int, operation: str, output: str,
	rotate: int, flip: str, title: str, cbar_title: str
):
	"""mhd/raw file viewer

	\b
	examples:
	basic usage         mhdview file.mhd
	with background     mhdview -b bg.mhd file.mhd
	with colour         mhdview file.mhd -c
	with threshold (%)  mhdview -c -t2 file.mhd
	"""

	if cmap != '' and cmap not in mpl.colormaps:
		mhd_files = (click.Path(exists=True)(cmap),) + mhd_files
		cmap = 'jet'

	if len(mhd_files) == 0:
		raise click.MissingParameter('at least one mhd file is required')
	elif len(mhd_files) > 1 and operation == '':
		raise click.BadParameter('multiple mhd files but no operation specified')

	nopts = 0
	nopts = nopts + (1 if lnormalise else 0)
	nopts = nopts + (1 if normalise else 0)
	nopts = nopts + (1 if clamp is not None else 0)
	if nopts > 1:
		raise click.BadParameter('only one of (-n, -N, -m) is possible')

	mhd_view = MhdView(cmap, alpha, threshold)
	mhd_view.set_defaults(default_axis, default_depth)
	mhd_view.set_rot(rotate)
	mhd_view.set_flip(flip)

	if clamp is not None:
		mhd_view.set_normalise(clamp)
	elif normalise:
		mhd_view.set_normalise('global')
	elif lnormalise:
		mhd_view.set_normalise('slice')

	mhd_view.set_cbar_title(cbar_title)
	mhd_view.open(mhd_files, background_mhd, operation, log=log)
	mhd_view.set_title(mhd_files[0] if title == 'auto' else title)

	if output == '':
		mhd_view.set_step(step)
		mhd_view.view()
	else:
		mhd_view.save(output, dpi=300)

	mhd_view.close()


mpl.use('tkagg')

if __name__ == '__main__':
	main()
