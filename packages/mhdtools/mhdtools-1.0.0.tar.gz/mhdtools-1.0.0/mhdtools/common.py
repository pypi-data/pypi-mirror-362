#!/usr/bin/env python3

import numpy as np
import SimpleITK as sitk
from scipy import ndimage


def to_axial(img):
	return img


def to_sagittal(img):
	return np.rot90(np.swapaxes(img, 0, 2), axes=(1, 2))


def to_coronal(img):
	return np.flip(np.swapaxes(img, 0, 1), 1)


to_plan = {'axial': to_axial, 'sagittal': to_sagittal, 'coronal': to_coronal}
to_plan_index = {'axial': 2, 'sagittal': 1, 'coronal': 0}
plans = list(to_plan.keys())


def is_valid_plan(axis):
	return axis in plans


def raw_plan(raw, axis):
	return np.array(to_plan[axis](raw))


def raw_slice(raw, axis, slice_number):
	return np.array(raw_plan(raw, axis)[slice_number])


def try_3d_projection(a):
	return a.squeeze()


def load_data(mhd):
	img = sitk.ReadImage(mhd)
	array = np.array(sitk.GetArrayFromImage(img))
	if len(array.shape) == 4:
		array = try_3d_projection(array)
	return array, img.GetOrigin(), img.GetSpacing()


def load(mhd, axis):
	data, origin, spacing = load_data(mhd)
	origin = origin[to_plan_index[axis]]
	spacing = spacing[to_plan_index[axis]]
	data = to_plan[axis](data)
	return np.array(data), origin, spacing


def load_slice(mhd, axis, slice_number):
	data, origin, spacing = load_data(mhd)
	origin = [x for i, x in enumerate(origin) if i != to_plan_index[axis]]
	spacing = [x for i, x in enumerate(spacing) if i != to_plan_index[axis]]
	data = to_plan[axis](data)
	return np.array(data[slice_number]), origin, spacing


def to_color_v(value, color):
	return color if value > .5 else [0., 0., 0., 0.]


def to_color(a, color):
	w, h = a.shape
	return [[to_color_v(a[x, y], color) for y in range(h)] for x in range(w)]


def if_(a, predicate):
	w, h = a.shape
	return [[1. if predicate(a[x, y]) else 0. for y in range(h)] for x in range(w)]


# Edge filters
vfilter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], np.float32)
hfilter = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], np.float32)


def edges(data):
	vedges = abs(ndimage.convolve(data, vfilter))
	hedges = abs(ndimage.convolve(data, hfilter))
	return np.maximum(vedges, hedges)
