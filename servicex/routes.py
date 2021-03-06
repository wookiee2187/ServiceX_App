# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


def add_routes(api, transformer_manager, rabbit_mq_adaptor,
               object_store, elasticsearch_adapter, code_gen_service,
               lookup_result_processor):
    from servicex.resources.submit_transformation_request import SubmitTransformationRequest
    from servicex.resources.transform_start import TransformStart
    from servicex.resources.transform_status import TransformationStatus
    from servicex.resources.file_transform_status import FileTransformationStatus
    from servicex.resources.query_transformation_request import QueryTransformationRequest
    from servicex.resources.add_file_to_dataset import AddFileToDataset
    from servicex.resources.preflight_check import PreflightCheck
    from servicex.resources.fileset_complete import FilesetComplete
    from servicex.resources.transformer_file_complete import TransformerFileComplete

    SubmitTransformationRequest.make_api(rabbitmq_adaptor=rabbit_mq_adaptor,
                                         object_store=object_store,
                                         elasticsearch_adapter=elasticsearch_adapter,
                                         code_gen_service=code_gen_service,
                                         lookup_result_processor=lookup_result_processor)
    api.add_resource(SubmitTransformationRequest, '/servicex/transformation')

    api.add_resource(QueryTransformationRequest,
                     '/servicex/transformation/<string:request_id>',
                     '/servicex/transformation')

    api.add_resource(TransformationStatus,
                     '/servicex/transformation/<string:request_id>/status')
    api.add_resource(FileTransformationStatus,
                     '/servicex/transformation/<string:request_id>/<int:file_id>/status')

    AddFileToDataset.make_api(lookup_result_processor, elasticsearch_adapter)
    api.add_resource(AddFileToDataset, '/servicex/transformation/<string:request_id>/files')

    PreflightCheck.make_api(lookup_result_processor)
    api.add_resource(PreflightCheck, '/servicex/transformation/<string:request_id>/preflight')

    FilesetComplete.make_api(lookup_result_processor)
    api.add_resource(FilesetComplete, '/servicex/transformation/<string:request_id>/complete')

    TransformStart.make_api(transformer_manager)
    api.add_resource(TransformStart, '/servicex/transformation/<string:request_id>/start')

    TransformerFileComplete.make_api(transformer_manager, elasticsearch_adapter)
    api.add_resource(TransformerFileComplete,
                     '/servicex/transformation/<string:request_id>/file-complete')
