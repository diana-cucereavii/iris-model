FROM public.ecr.aws/lambda/python:3.7
# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
COPY ./iris_trained_model.pkl ${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
#RUN pip3 install -U scikit-learn scipy matplotlib numpy
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
# EXPOSE 80
# ENTRYPOINT ["python", "app.py"]

