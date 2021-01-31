package utils

type Vector []float64

// Add the elements of two vectors.
func (a Vector) AddVec(b Vector) Vector {
	v_new := make(Vector, len(a))
	for idx, _ := range a {
		v_new[idx] = a[idx] + b[idx]
	}
	return v_new
}

// Multiply every element of a vector by a scalar.
func (a Vector) MultTime(b float64) Vector {
	v_new := make(Vector, len(a))
	for idx, a_i := range a {
		v_new[idx] = a_i * b
	}
	return v_new
}

// Multiply two vectors element-wise (dot product).
func (a Vector) MultVec(b Vector) Vector {
	v_new := make(Vector, len(a))
	for idx, _ := range a {
		v_new[idx] = a[idx] * b[idx]
	}
	return v_new
}

// Add a scalar to each element of a vector.
func (a Vector) AddTime(b float64) Vector {
	v_new := make(Vector, len(a))
	for idx, a_i := range a {
		v_new[idx] = a_i + b
	}
	return v_new
}
