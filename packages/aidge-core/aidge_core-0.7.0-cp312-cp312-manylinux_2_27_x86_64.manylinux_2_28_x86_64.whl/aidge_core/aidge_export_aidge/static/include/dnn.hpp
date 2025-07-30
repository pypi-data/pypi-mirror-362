#ifndef DNN_HPP
#define DNN_HPP
#include <aidge/graph/GraphView.hpp>
/**
 * @brief This file contains all of what is related to the construction of the
 * neural network
 *
 */

/**
 * @brief This function generate the exported Aidge::GraphView.
 *
 * @return std::shared_ptr<Aidge::GraphView>
 */
std::shared_ptr<Aidge::GraphView> generateModel();

#endif /* DNN_HPP */
