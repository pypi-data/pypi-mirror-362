use numpy::PyReadonlyArray2;
use pyo3::{pyfunction, pymodule, wrap_pyfunction, Bound};
use pyo3::types::PyList;
use pyo3::prelude::*;
use rayon::prelude::*;


#[pyfunction]
fn _colour_strings_with_newlines_rust(py: Python<'_>, theimage: PyReadonlyArray2<'_, i64>, rgb_lookup: Vec<String>) -> PyResult<PyObject> {
    let theimage_array = theimage.as_array();
    let shape = theimage_array.shape();
    let (rows, cols) = (shape[0], shape[1]);

    // Parallelize over row pairs
    let result: Vec<String> = (1..rows)
        .into_par_iter()
        .step_by(2)
        .flat_map_iter(|row| {
            let mut row_strings = Vec::with_capacity(cols + 1);
            for col in 0..cols {
                let upper_value = &rgb_lookup[theimage_array[[row - 1, col]] as usize];
                let lower_value = &rgb_lookup[theimage_array[[row, col]] as usize];
                row_strings.push(format!("{} on {}", lower_value, upper_value));
            }
            row_strings.push("\n".to_string());
            row_strings
        })
        .collect();

    Ok(PyList::new(py, &result)?.into())
}


#[pymodule]
#[pyo3(name = "climax_rs")]
fn rust_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_colour_strings_with_newlines_rust, m)?)?;

    Ok(())
}
