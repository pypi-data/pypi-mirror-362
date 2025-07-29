FROM ghcr.io/ewatercycle/remotebmi-julia:0.1.0

LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/ewatercycle-wflowjl"

# Install Wflow
RUN julia -e 'using Pkg; Pkg.add(PackageSpec(name="Wflow", version="0.8.1"))'

RUN echo "using Wflow" > run.jl
RUN echo "import RemoteBMI.Server: run_bmi_server" >> run.jl
RUN echo "port = parse(Int, get(ENV, \"BMI_PORT\", \"50051\"))" >> run.jl
RUN echo "run_bmi_server(Wflow.Model, \"0.0.0.0\", port)" >> run.jl

# chmod central depot path so all users can access it
RUN chmod -R 777 ${JULIA_DEPOT_PATH}

# Expose port and start server
EXPOSE 50051
CMD ["julia", "run.jl"]
