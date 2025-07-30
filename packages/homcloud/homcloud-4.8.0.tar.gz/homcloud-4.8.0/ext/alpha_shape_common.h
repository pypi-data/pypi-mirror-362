#ifndef HOMCLOUD_ALPHA_SHAPE_COMMON_H
#define HOMCLOUD_ALPHA_SHAPE_COMMON_H

// Some common functions for alpha_shape_3 and alpha_shape_2
static bool ArrayHasCorrectShape(PyArrayObject* points, int dim, int weighted,
                                 int rel_homology) {
  npy_intp* dims = PyArray_DIMS(points);
  int correct_2nd_dim = dim + weighted + rel_homology;

  if ((PyArray_NDIM(points) == 2) && (dims[1] == correct_2nd_dim))
    return true;
  
  PyErr_SetString(PyExc_ValueError, "Wrong shape of array");
  return false;
}

template<typename Types, typename Element, typename Iterator, typename Creator>
PyObject* AlphaShape_tolist(
  typename Types::AlphaShape* self,
  Iterator begin, Iterator end, int num_elements, Creator create) {
  
  PyObject* list = PyList_New(num_elements);
  if (!list) return NULL;
  
  int index = 0;
  for (Iterator iter = begin; iter != end; ++iter, ++index) {
    Element* element = create(self, iter);
    if (!element) goto error;
    if (PyList_SetItem(list, index, cast_PyObj(element)) < 0)
      goto error;
  }
  
  return list;

error:
  Py_DECREF(list);
  return NULL;
}

static PyObject* method_return_true(PyObject* self) {
  Py_RETURN_TRUE;
}

static PyObject* method_return_false(PyObject* self) {
  Py_RETURN_FALSE;
}

static int GroupName(int dim, PyArrayObject* points, int index, int weighted, int rel_homology) {
  if (rel_homology)
    return static_cast<int>(*GETPTR2D<double>(points, index, dim + weighted));
  else
    return -1;
}

#endif // HOMCLOUD_ALPHA_SHAPE_COMMON_H
