import layerx
api_key = 'key_oat98bmu2awv5gfq6m3li3ovdxxr6qpt'
secret = 'urq0szzs3io7hbvlpbqu'
url = 'http://localhost'
client = layerx.LayerxClient(api_key, secret, url)
meta_data_object = {
    "meta_data": {
        "test": "test_1",
    }
}

'''
upload_res = client.upload_files_to_collection('/Users/kelumvithana/My Projects/AnnotationTool/LayerX/python-sdk/layerx-python-sdk/uploads', "image", "Hot Air Balloons", meta_data_object)

#upload_res = client.upload_annoations_for_folder('/Users/kelumvithana/My Projects/AnnotationTool/LayerX/python-sdk/uploads', "image", "Open_Images_2", meta_data_object, False)
#upload_res = client.upload_files_to_collection('/Users/kelumvithana/My Projects/AnnotationTool/LayerX/python-sdk/uploads', "image", "Open_Images_2", meta_data_object)
print(upload_res)
jobid = upload_res['job_id']
collid = upload_res['collection_id']
print('Waiting.... for job ' + jobid)
client.wait_for_job_complete(jobid)
print('Upload Waiting end.')


project_res = client.create_annotation_project_from_collection("Hot Air Balloon Annotation", "6408740b7e9f37e50f15b7ed")
job_id = project_res['job_id']
project_id = project_res['id']
print(project_id)
print('Waiting.... for job ' + job_id)
client.wait_for_job_complete(job_id)
print('Upload Waiting end.')
'''

client.upload_annoations_for_folder('Hot Air Balloons', 'Hot_air_balloon_model_run_1.0.1', 'annotations/raw.json', 'rectangle', True, True, '640875914e1dd5e5a55e5e87')

#client.upload_annoations_for_folder('Vehicle_Demo', 'road-traffic-model_001', 'Vehicle_Demo_raw/Vehicle_Demo_raw.json', 'rectangle', False, True)

#client.download_project_annotations("63da59032798fcdaf602a0f0", ['accepted'], True, '/Users/kelumvithana/My Projects/AnnotationTool/LayerX/python-sdk/layerx-python-sdk/tests/earth')
#client.download_project_annotations("63da59032798fcdaf602a0f0", ['qa_completed'])

#client.remove_annotations("63ee122478a4f8648d128fed", "63ee1b193f35ac5ffcab15bb")
