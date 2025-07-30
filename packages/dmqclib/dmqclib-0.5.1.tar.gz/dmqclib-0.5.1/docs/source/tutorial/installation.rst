Step 1: Installation
========================

The ``dmqclib`` library can be installed using several popular Python package managers. We recommend an approach that combines `mamba` and `uv` for the best performance and dependency management, particularly in complex environments. However, standard installation methods using `pip` or `conda` are also fully supported.

Recommended Approach: Mamba + uv
---------------------------------
This method is highly recommended for all users, especially those managing multiple projects or complex dependencies. `Mamba <https://mamba.readthedocs.io/>`_ is a fast, drop-in replacement for ``conda``, offering superior speed and reliability for environment and package management. `uv <https://docs.astral.sh/uv/>`_ is an extremely fast Python package installer and resolver, ensuring quick and efficient dependency resolution.

**Benefits of this approach:**
*   **Speed:** Significantly faster environment and package installations.
*   **Reliability:** Robust dependency resolution, reducing conflicts.
*   **Isolation:** Creates a dedicated environment for ``dmqclib``, preventing conflicts with other Python projects.

**Step 1: Create and activate a new environment with Mamba**

This command creates a new, isolated environment named ``dmqclib-env`` and pre-installs Python and `uv` from the `conda-forge` channel.

.. code-block:: bash

   # Create a new environment named 'dmqclib-env'
   mamba create -n dmqclib-env -c conda-forge python=3.12 uv

   # Activate the newly created environment
   # On Linux/macOS:
   mamba activate dmqclib-env
   # On Windows (in Anaconda Prompt or cmd.exe):
   # conda activate dmqclib-env

.. important::
   Remember to activate ``dmqclib-env`` every time you wish to use ``dmqclib`` to ensure you are working within the correct, isolated environment.

**Step 2: Install dmqclib using uv**

Once you are inside the activated ``dmqclib-env`` environment, use `uv` to install the ``dmqclib`` package and its dependencies from PyPI.

.. code-block:: bash

   uv pip install dmqclib


Alternative Approaches
----------------------
If the recommended `mamba` + `uv` approach doesn't fit your workflow, you can use one of the following standard methods.

Using pip
~~~~~~~~~
You can install ``dmqclib`` directly from PyPI using ``pip``.

.. note::
   It is highly recommended to install the package inside a virtual environment (like `venv` or `virtualenv`) to avoid conflicts with other projects or system packages. This is crucial for managing Python dependencies effectively.

.. code-block:: bash

   pip install dmqclib

Using conda or mamba (from conda-forge)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``dmqclib`` package is available on the `conda-forge` channel, which is the recommended community-maintained channel for Conda packages. You can use either ``conda`` or ``mamba`` to install it.

.. code-block:: bash

   # Using conda (creates a new environment if 'dmqclib' is not found globally)
   conda install -c conda-forge dmqclib

   # Or using mamba (for a faster installation and better dependency resolution)
   mamba install -c conda-forge dmqclib

.. tip::
   While ``dmqclib`` might also be indexed on other Anaconda channels (e.g., `takayasaito`), we strongly recommend using `conda-forge` for consistency, broader dependency availability, and community support.

Using uv (Standalone for virtual environments)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you prefer to use `uv` for both creating virtual environments and installing packages, follow these steps. This method is an excellent pure-Python alternative for environment and package management.

**Step 1: Create and activate a virtual environment with uv**

`uv` will create a new virtual environment in a `.venv` directory within your current working directory by default.

.. code-block:: bash

   # Create a virtual environment
   uv venv

   # Activate it (on Linux/macOS):
   source .venv/bin/activate
   # On Windows (in Command Prompt/PowerShell):
   # .venv\Scripts\activate

**Step 2: Install dmqclib**

Once your `uv`-managed virtual environment is activated, proceed with the installation:

.. code-block:: bash

   uv pip install dmqclib

Next Steps
----------
You have now successfully installed the ``dmqclib`` library! The next step in your journey is to understand how to prepare your raw data into a format suitable for model training.

Proceed to the next tutorial: :doc:`./preparation`.
