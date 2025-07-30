
#include <iostream>
#include <vector>
#include "wignerSymbols.h"
#include "pybind11/numpy.h"
#include "func.hpp"
namespace py= pybind11; 
std::vector<std::vector<double>> Wignerindex(int l) {
    std::vector<std::vector<double>> selected;
    
    for (int m1 = -l; m1 <= l; ++m1) {
        for (int m2 = -l; m2 <= l; ++m2) {
            const int m3 = - (m1 + m2);
            if (m3 < -l || m3 > l) continue;
            double windex = WignerSymbols::wigner3j(l, l, l, m1, m2, m3);
            selected.push_back({static_cast<double>(m1),
                               static_cast<double>(m2),
                               static_cast<double>(m3),
                               windex});
        }
    }
    return selected;

}



std::vector<std::complex<double>> SphHarm6(double theta, double phi) {
    std::vector<std::complex<double>> results;
    
    // m = -6
    results.push_back((1.0/64.0) * std::sqrt(3003.0/M_PI) 
                     * std::polar(1.0, -6.0*phi) 
                     * std::pow(std::sin(theta), 6));
    
    // m = -5
    results.push_back((3.0/32.0) * std::sqrt(1001.0/M_PI) 
                     * std::polar(1.0, -5.0*phi) 
                     * std::pow(std::sin(theta), 5) * std::cos(theta));
    
    // m = -4
    results.push_back((3.0/32.0) * std::sqrt(91.0/(2*M_PI)) 
                     * std::polar(1.0, -4.0*phi) 
                     * std::pow(std::sin(theta), 4) 
                     * (11.0*std::pow(std::cos(theta), 2) - 1.0));
    
    // m = -3
    results.push_back((1.0/32.0) * std::sqrt(1365.0/M_PI) 
                     * std::polar(1.0, -3.0*phi) 
                     * std::pow(std::sin(theta), 3) 
                     * (11.0*std::pow(std::cos(theta), 3) - 3.0*std::cos(theta)));
    
    // m = -2
    results.push_back((1.0/64.0) * std::sqrt(1365.0/M_PI) 
                     * std::polar(1.0, -2.0*phi) 
                     * std::pow(std::sin(theta), 2) 
                     * (33.0*std::pow(std::cos(theta), 4) - 18.0*std::pow(std::cos(theta), 2) + 1.0));
    
    // m = -1
    results.push_back((1.0/16.0) * std::sqrt(273.0/(2*M_PI)) 
                     * std::polar(1.0, -1.0*phi) * std::sin(theta) 
                     * (33.0*std::pow(std::cos(theta), 5) - 30.0*std::pow(std::cos(theta), 3) + 5.0*std::cos(theta)));
    
    // m = 0
    results.push_back((1.0/32.0) * std::sqrt(13.0/M_PI) 
                     * (231.0*std::pow(std::cos(theta), 6) 
                        - 315.0*std::pow(std::cos(theta), 4) 
                        + 105.0*std::pow(std::cos(theta), 2) 
                        - 5.0));
    
    // m = 1
    results.push_back(-(1.0/16.0) * std::sqrt(273.0/(2*M_PI)) 
                     * std::polar(1.0, 1.0*phi) * std::sin(theta) 
                     * (33.0*std::pow(std::cos(theta), 5) - 30.0*std::pow(std::cos(theta), 3) + 5.0*std::cos(theta)));
    
    // m = 2
    results.push_back((1.0/64.0) * std::sqrt(1365.0/M_PI) 
                     * std::polar(1.0, 2.0*phi) 
                     * std::pow(std::sin(theta), 2) 
                     * (33.0*std::pow(std::cos(theta), 4) - 18.0*std::pow(std::cos(theta), 2) + 1.0));
    
    // m = 3
    results.push_back(-(1.0/32.0) * std::sqrt(1365.0/M_PI) 
                     * std::polar(1.0, 3.0*phi) 
                     * std::pow(std::sin(theta), 3) 
                     * (11.0*std::pow(std::cos(theta), 3) - 3.0*std::cos(theta)));
    
    // m = 4
    results.push_back((3.0/32.0) * std::sqrt(91.0/(2*M_PI)) 
                     * std::polar(1.0, 4.0*phi) 
                     * std::pow(std::sin(theta), 4) 
                     * (11.0*std::pow(std::cos(theta), 2) - 1.0));
    
    // m = 5
    results.push_back(-(3.0/32.0) * std::sqrt(1001.0/M_PI) 
                     * std::polar(1.0, 5.0*phi) 
                     * std::pow(std::sin(theta), 5) * std::cos(theta));
    
    // m = 6
    results.push_back((1.0/64.0) * std::sqrt(3003.0/M_PI) 
                     * std::polar(1.0, 6.0*phi) 
                     * std::pow(std::sin(theta), 6));

    return results;
}