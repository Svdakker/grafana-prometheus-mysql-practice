FROM bitnami/grafana:11.3.0

# Switch to root to install Python
USER root

# Install Python
RUN install_packages python3 python3-pip netcat-traditional

USER 1001

# Start Grafana
ENTRYPOINT ["/bin/sh", "-c", "/opt/bitnami/scripts/grafana/run.sh"]
