FROM public.ecr.aws/lambda/python:3.9

RUN echo ${LAMBDA_TASK_ROOT}

# Copy function code
ARG zip_path 

RUN yum install -y unzip

COPY ${zip_path} ${LAMBDA_TASK_ROOT}
 
RUN unzip ${LAMBDA_TASK_ROOT}/${zip_path} -d ${LAMBDA_TASK_ROOT}
                  
RUN rm  -f ${LAMBDA_TASK_ROOT}/${zip_path}

#RUN cp -f ${LAMBDA_TASK_ROOT}/handler.py 
RUN ls -l
CMD ["handler.hello"] 
