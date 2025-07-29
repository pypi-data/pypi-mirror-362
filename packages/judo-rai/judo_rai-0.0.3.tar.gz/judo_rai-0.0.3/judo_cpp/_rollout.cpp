#include <cmath>
#include <vector>
#include <array>
#include <functional>
#include <iostream>
#include <mujoco/mujoco.h>


struct RolloutData
{
    std::vector<double> states;
    std::vector<double> sensors;
    std::vector<double> inputs;
};

void Rollout(const mjModel* model, mjData* data, int steps, RolloutData& rd) {
    int nq      = model->nq;
    int nv      = model->nv;
    int nu      = model->nu;
    int nsens   = model->nsensordata;
    int nstates = nq + nv;

    // allocate storage
    rd.states.resize(steps * nstates);
    rd.inputs.resize(steps * nu);
    rd.sensors.resize(steps * nsens);

    for (int i = 0; i < steps; i++) {
        mj_step(model, data);

        // states
        for (int j = 0; j < nq; j++) {
            rd.states[i*nstates + j] = data->qpos[j];
        }
        for (int j = 0; j < nv; j++) {
            rd.states[i*nstates + nq + j] = data->qvel[j];
        }

        // sensors
        for (int j = 0; j < nsens; j++) {
            rd.sensors[i*nsens + j] = data->sensordata[j];
        }

        // controls
        for (int j = 0; j < nu; j++) {
            rd.inputs[i*nu + j] = data->ctrl[j];
        }
    }
}

void ParallelRollout(std::vector<const mjModel*>& models,
                     std::vector<mjData*> data,
                     int steps,
                     std::vector<RolloutData>& rd) {
    #pragma omp parallel for
    for (int i = 0; i < models.size(); i++) {
        Rollout(models[i], data[i], steps, rd[i]);
    }
}

// void ParallelRollout(py::list model, mjData* data,  mjtNum* x0, mjtNum* ctrl) {
//     #pragma omp parallel for
//     for (int i = 0; i < models.size(); i++) {
//         Rollout(models[i], data[i], steps, rd[i]);
//     }
// }
