#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/functional.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

void _verlet_mapping_variables(
    Eigen::VectorXd& x,
    Eigen::VectorXd& p,
    const Eigen::MatrixXd& H,
    double dt,
    int nlit)
{
    const Eigen::MatrixXd H_T = H.transpose();

    Eigen::VectorXd dpdt(x.size());
    Eigen::VectorXd dxdt(x.size());
    Eigen::VectorXd d2xdt2(x.size());

    const double dt_squared = dt * dt;

    for (int istep = 0; istep < nlit; ++istep) {
        // --- Calculate initial derivatives using optimized matrix-vector products ---
        dpdt = -H_T * x;
        dxdt = H_T * p;
        d2xdt2 = H_T * dpdt;

        // --- First half of the Verlet integration step ---
        // Eigen overloads operators for efficient, fused vector arithmetic.
        p += 0.5 * dt * dpdt;
        x += dt * dxdt + 0.5 * dt_squared * d2xdt2;

        // --- Recalculate dpdt with the updated position x ---
        dpdt = -H_T * x;

        // --- Second half of the Verlet integration step ---
        p += 0.5 * dt * dpdt;
    }
}

void linearized_dynamics(
    Eigen::VectorXd& x_bath,
    Eigen::VectorXd& p_bath,
    Eigen::VectorXd& x_map,
    Eigen::VectorXd& p_map,
    double dt_bath,
    int nstep,
    int dump,
    int nlit,
    Eigen::MatrixXd& ham,
    const py::object& system_callback)
    //    const py::object& bath_force,
    //    const py::object& system_hamiltonian,
    //    const py::object& bath_callback)
{
    // Pre-calculate constants to avoid repeated floating-point operations in the loop.
    const double dt_bath_half = 0.5 * dt_bath;
    const double dt_bath_sq_half = 0.5 * dt_bath * dt_bath;

    // Calculate the initial force on the bath before the loop starts.
    int itime = 0;
//    Eigen::VectorXd force = bath_force(x_bath, x_map, p_map).cast<Eigen::VectorXd>();

    for (int istep = 1; istep <= nstep; ++istep) {
        // --- First half of the bath's Verlet step ---
        //        x_bath += p_bath * dt_bath + force * dt_bath_sq_half;
        //        p_bath += force * dt_bath_half;

        // --- Update system Hamiltonian and propagate mapping variables ---
        //        Eigen::MatrixXd ham = system_hamiltonian(x_bath).cast<Eigen::MatrixXd>();
        //        _verlet_mapping_variables(x_map, p_map, ham, dt_bath/nlit, nlit);

        // --- Calculate the reduced density matrix at specified dump intervals ---
        if (istep % dump == 0) {
            itime++;
            system_callback(x_map, p_map);
            //            bath_callback(x_bath, p_bath);
        }

        // --- Update the force and complete the bath's Verlet step ---
        //        force = bath_force(x_bath, x_map, p_map).cast<Eigen::VectorXd>();
        //        p_bath += force * dt_bath_half;
    }
}

PYBIND11_MODULE(_mqds, m) {
    m.doc() = R"pbdoc(
        Pybind11 MQDS plugin
        -----------------------

        .. currentmodule:: _mqds

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("add", &add,
    R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc"
    );

    m.def("linearized_dynamics", &linearized_dynamics,
    R"pbdoc(
        Linearized dynamics

        Propagation with a linearized approximation to the dynamics.
    )pbdoc"
    );

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
