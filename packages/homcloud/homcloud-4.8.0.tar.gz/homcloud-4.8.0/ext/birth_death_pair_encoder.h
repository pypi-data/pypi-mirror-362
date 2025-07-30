#ifndef HOMCLOUD_BIRTH_DEATH_PAIR_ENCODER_H
#define HOMCLOUD_BIRTH_DEATH_PAIR_ENCODER_H

struct ListOfTupleEncoder {
  PyObject* list_;
  bool stopped_;
  ListOfTupleEncoder(): list_(PyList_New(0)), stopped_(false) {}

  void AddTuple(PyObject* tuple) {
    if (!tuple) {
      stopped_ = true; 
      return;
    }
    if (PyList_Append(list_, tuple) < 0)
      stopped_ = true;
    Py_CLEAR(tuple);
  }

  void AddPair(int8_t dim, int64_t birth, int64_t death) {
    if (stopped_) return;
    AddTuple(Py_BuildValue("(bll)", dim, birth, death));
  }

  void AddEssentialPair(int8_t dim, int64_t birth) {
    if (stopped_) return;
    AddTuple(Py_BuildValue("(blO)", dim, birth, Py_None));
  }

  bool IsAllocationError() {
    return list_ == nullptr;
  }
};

#endif // HOMCLOUD_BIRTH_DEATH_PAIR_ENCODER_H
