import cv2 
import os    
import subprocess

subtitle_frame = [
    "Screenshots_2023-11-07T15-23-43.png", ## song_title  0 to 450 
    "Screenshots_2023-11-07T15-25-12.png", # sk1 sloka start form 450
    "Screenshots_2023-11-07T15-25-21.png", # sk2 1339
    "Screenshots_2023-11-07T15-25-28.png", # sk3 2200 
    "Screenshots_2023-11-07T15-25-36.png", # sk4 3339
    "Screenshots_2023-11-07T15-25-43.png", # sk5 4185
    "Screenshots_2023-11-07T15-25-45.png", # sk6 5057
    "Screenshots_2023-11-07T15-26-00.png", # sk7 6039 
    "Screenshots_2023-11-07T15-26-37.png", # sk8 7077
    "Screenshots_2023-11-07T15-26-46.png", # sk9 7918
    "Screenshots_2023-11-07T14-57-28.png", # music 8813, 
    "Screenshots_2023-11-07T15-26-53.png", # sk10 9115  
    "Screenshots_2023-11-07T15-27-00.png", # sk11 9962
    "Screenshots_2023-11-07T15-27-06.png", # sk12 10816
    "Screenshots_2023-11-07T14-57-28.png", #  music 11677,     
    "Screenshots_2023-11-07T15-27-13.png", # sk13 12487
    "Screenshots_2023-11-07T15-27-20.png", # sk14 13400
    "Screenshots_2023-11-07T15-27-27.png", # sk15 14280
    "Screenshots_2023-11-07T15-27-33.png", # sk16 15352
    "Screenshots_2023-11-07T15-27-41.png", # sk17 16282
    "Screenshots_2023-11-07T15-27-54.png", # sk18 17151
    "Screenshots_2023-11-07T14-57-28.png", # music 18011
    "Screenshots_2023-11-07T15-28-23.png", # sk19 18329
    "Screenshots_2023-11-07T15-28-32.png", # sk20 19175
    "Screenshots_2023-11-07T15-28-38.png"  # sk21 20052
] # last_frame : 21422

subtitle_list= [0,450,1339,2200,3339,4185,5057,6039,7077,7918,8813,9115,9962,10816,11677,12487,13400, 14280, 15352, 16282, 17151, 18011, 18329, 19175, 20052, 21422]

sub_title_dir = 'lyrics-imgs'

frame_dir = 'recorded-video' 
frame_img_reg = '%06d.png'
frame_rate = '25'
screen_aspect_ratio = '1280x720'
output_video = 'output4.mp4'
resolution = 'yuv420p'  # pixel formate 720p

# create dir/folder if not exist
if not os.path.exists(frame_dir):
   os.makedirs(frame_dir)


padding = '06'
path = os.getcwd() 

for frame_idx in range(0,subtitle_list[-1]+1):
    frame_name = f'{frame_idx:06}.png'
    for  idx, frame in enumerate(subtitle_list) :
        if frame_idx > frame :
            continue
        else:
            subtitle_idx = idx
            break
    if idx ==0:
        # if idx = 0 then sub-title image : will be set to index = -1 {subtitle_frame[idx]-1}=> which will last image as `00000.png` 
        # so we remove -1 
        print(f"'{frame_idx}/{subtitle_list[-1]+1}:{frame_idx/(subtitle_list[-1]+1):.2f}%  frame_idx='{frame_idx}' frame:{frame}, subtitle no {idx} , subtitle name : {subtitle_frame[idx]}, idx={idx}" )
        image2 = cv2.imread(f'{sub_title_dir}/{subtitle_frame[idx]}')
    # cv2.imwrite(f'{frame_dir}/{frame_name}', image2)
    else:
        print(f"[{100*frame_idx/(subtitle_list[-1]+1):.2f}% ]:{frame_idx}/{subtitle_list[-1]+1}  frame_idx='{frame_idx}' frame:{frame}, subtitle no {idx-1} , subtitle name : {subtitle_frame[idx-1]}, idx={idx}" )
    #    print(frame_idx, idx)
        image2 = cv2.imread(f'{sub_title_dir}/{subtitle_frame[idx-1]}')
    cv2.imwrite(f'{frame_dir}/{frame_name}', image2)

shell_cmd =f'ffmpeg -i {frame_dir}/{frame_img_reg} -c:v libx264 -r {frame_rate} -s {screen_aspect_ratio}  -pix_fmt {resolution} {output_video}'
subprocess.run (shell_cmd,shell=True,  stdout=subprocess.PIPE)

# delete the frame_dir folder with all `frame images`

shell_cmd= f'rm -rf {frame_dir}
print(shell_cmd)
#subprocess.run (shell_cmd,shell=True,  stdout=subprocess.PIPE)
