
poetry build .
pip3 uninstall --break-system-packages code-agent
pip3 install --break-system-packages .
