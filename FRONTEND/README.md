# MethodSolver - Numerical Analysis Final Project (Frontend)

## Content Table
- [MethodSolver - Numerical Analysis Final Project (Frontend)](#methodsolver---numerical-analysis-final-project-frontend)
  - [Content Table](#content-table)
  - [Authors](#authors)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Setup Instructions](#setup-instructions)
    - [Clone the repository:](#clone-the-repository)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
    - [Implemented Numerical Methods:](#implemented-numerical-methods)
  - [Contribution](#contribution)
  - [License](#license)
  - [Contact](#contact)

## Authors

- Kevin Quiroz González
- Juan Felipe Restrepo

## Introduction

The frontend of MethodSolver is a web-based interface designed to facilitate the use of various numerical methods learned in the Numerical Analysis course at EAFIT University. It provides a user-friendly interface where users can input data, view mathematical results in LaTeX format, and visualize graphs of functions using GeoGebra.

## Project Structure
```plaintext
frontend/
├── app/                           # Application base code
│   ├── __pycache__/               # Python cache files
├── static/                        # Static files (CSS, JS, images)
│   ├── css/                       # Custom CSS files
│   │   ├── guia.css
│   │   ├── styles.css
│   │   └── test.css
│   ├── images/                    # Image resources
│   └── js/                        # JavaScript files for each method
│       ├── bisection.js
│       ├── factorization_lu.js
│       ├── false_rule.js
│       ├── fixed_point.js
│       ├── gauss_elimination.js
│       ├── gauss_seidel_method.js
│       ├── graph.js
│       ├── jacobi_method.js
│       ├── lagrange.js
│       ├── modified_newton.js
│       ├── newton_raphson.js
│       ├── newton.js
│       ├── secant.js
│       ├── second_modified_newton.js
│       ├── sor_method.js
│       ├── spline.js
│       └── vandermonde.js
└── templates/                     # HTML templates for each method
    ├── bisection.html
    ├── factorization_lu.html
    ├── false_rule.html
    ├── first_modified_newton.html
    ├── fixed_point.html
    └── ... (other HTML templates)
```
## Setup Instructions
To set up the frontend of this project locally, follow these steps:

### Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/NumericalAnalysisFinalProject.git
cd NumericalAnalysisFinalProject/FRONTEND
```

## Technologies Used
- **HTML5 & CSS3:** Provides the basic structure and style of the web interface.
- **JavaScript (ES6):** Handles frontend logic, including data processing and API communication.
- **Bootstrap 5:** Ensures responsive design and layout.
- **GeoGebra API:** Renders interactive mathematical graphs.
- **MathJax:** Displays mathematical expressions in LaTeX format.

## Features

### Implemented Numerical Methods:
- Bisection Method
- False Position Method
- Newton Interpolation
- Lagrange Interpolation
- Spline Interpolation (Linear and Cubic)
- Gaussian Elimination
- Iterative Methods (Jacobi, Gauss-Seidel, SOR)
- LU Factorization
- Fixed-Point Iteration
- Secant Method
- Newton-Raphson Method
- ... and more

## Contribution

For contributing to this project, follow the instructions below:

1. **Fork the repository**: Make a fork of the repository and clone your fork on your local machine.
2. **Create a new branch**: Create a new branch with a name which gives an idea of the addition or correction to the project. 
3. **Make your changes**: Make your code changes and test them. 
4. **Make a pull request**: Finally, make a pull request to the original repository. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, feel free to reach out to:
- Juan Felipe Restrepo Buitrago: [jfrestrepb@eafit.edu.co](jfrestrepb@eafit.edu.co)
- Kevin Quiroz González: [kquirozg@eafit.edu.co](mailto:kquirozg@eafit.edu.co)

