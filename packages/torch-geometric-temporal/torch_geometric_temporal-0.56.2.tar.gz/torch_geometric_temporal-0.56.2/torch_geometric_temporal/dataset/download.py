import os
import ssl
import requests

PeMS_file_links = {
            "pems_cali_adj_mat.pkl" : "https://anl.app.box.com/shared/static/4143x1repqa1u26aiz7o2rvw3vpcu0wp",
            "pems_cali_speed.h5": "https://anl.app.box.com/shared/static/7hfhtie02iufy75ac1d8g8530majwci0"
        }          
        

        for key in PeMS_file_links.keys():
            
            # Check if file is in data folder from working directory, otherwise download
            if not os.path.isfile(
            os.path.join(self.raw_data_dir,key)
            ):
                print("Downloading ", key, flush=True)
                
                response = requests.get(PeMS_file_links[key], stream=True)
                file_size = int(response.headers.get('content-length', 0))

                with open(os.path.join(self.raw_data_dir, key), "wb") as file, tqdm(
                    total=file_size, unit="B", unit_scale=True, unit_divisor=1024
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=33554432):
                        file.write(chunk)
                        progress_bar.update(len(chunk))