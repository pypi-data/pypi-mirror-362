#include <cstdio>
#include <memory>

#include "aidge/backend/cpu.hpp"

/* Register default cpu Tensor implementation */
#include "aidge/backend/cpu/data/TensorImpl.hpp"

/* Include model generator */
#include "include/dnn.hpp"

int main()
{

    std::printf("BEGIN\n");

    std::shared_ptr<Aidge::GraphView> graph = generateModel();

    std::printf("END\n");

    return 0;
}
