
import sys

import flask
import numpy
import pandas
import sklearn
import networkx
import simpy
import matplotlib
import plotly
import psutil
import requests
import joblib
import pytest

print("=" * 45)
print(" AI NETWORK DIGITAL TWIN")
print(" ENVIRONMENT VERIFICATION")
print("=" * 45)

print("Python:", sys.version)
from importlib.metadata import version

print("Flask:", version("flask"))
print("NumPy:", numpy.__version__)
print("Pandas:", pandas.__version__)
print("Scikit-learn:", sklearn.__version__)
print("NetworkX:", networkx.__version__)
print("SimPy:", simpy.__version__)

print("\nAll libraries imported successfully!")
print("Environment setup completed.")
