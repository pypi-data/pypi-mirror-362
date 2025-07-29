# Base image with Python and tools
FROM public.ecr.aws/lambda/python:3.8 AS build

# Set working directory
WORKDIR /build

# Copy requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt -t .

# Copy lambda handler code
COPY . .

# Create deployment package (zip)
RUN zip -r9 /tmp/lambda_package.zip .

# Optional: expose final artifact
FROM alpine:3.18 as final
COPY --from=build /tmp/lambda_package.zip /lambda_package.zip
