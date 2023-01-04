import streamlit as st

import numpy as np
from PIL import Image
import os
import Data_Shop_CatsnDogs
import base64
from pathlib import Path

st.set_page_config("Animals Store", page_icon="dog", layout="wide")
sideb = st.sidebar

st.markdown("""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">""", unsafe_allow_html=True)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://camnang24h.net/wp-content/uploads/2018/11/hinh-nen-chu-meo-don-giang-sinh-merry-christmas-dep-17.jpg");
    background-size: cover;
}
</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)


st.markdown("""
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/">
  <img width="200" height="100" src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" class="header_logo header-logo entered lazyloaded" alt="Dogily Petshop – Bán chó mèo cảnh, thú cưng Tphcm, Hà nội" data-lazy-src="https://dogily.vn/wp-content/uploads/2020/07/dogily-logo.png" data-ll-status="loaded" target="_parent">
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/" target="_parent"><b>Home</b> <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Danh_Mục_Sản_Phẩm" target="_parent"><b>Danh Mục Sản Phẩm</b></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Tìm_Kiếm" target="_parent"><b>Tìm Kiếm</b></a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0" action="http://localhost:8501/T%C3%ACm_Ki%E1%BA%BFm">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
""", unsafe_allow_html=True)

st.markdown("""
            <style>
                .overlay{position: absolute;
                        display: flex;
                        top: 0;
                        bottom: 0;
                        left: 0;
                        right: 5;
                        align-items: center;
                        justify-content: center;
                        flex-direction: column;
                        color: white;
                        text-align: center;
                        }
                        .overlay .videoButtonWrapper{
                            flex-direction: row;
                            margin-bottom: 10px;
                        }
                        .videoBackgroundWrapper{position: relative; width: 100%;}
                        .videoBackground{width: 100%;}
                        .tooltip:hover .tooltiptext {
                            visibility: visible;
                }
                #container {
                    overflow: hidden;
                }
                #videobcg {
                    width: 1500px;
                    height: inherit;
                    -o-filter: brightness(70%);
                    filter: brightness(70%);
                    object-fit: cover;  
                    transform: scale(1.04);
                }
            </style>
            <div id="container">
                <video id="videobcg" preload="" playsinline="" autoplay="" muted="" loop="" class="stvideo">
                    <source src="https://dogily.vn/wp-content/uploads/2021/10/dogilybanner002.mp4" type="video/mp4">
                </video>
                <div class="overlay" >
                    <h1 style="font-size: 5rem" class="text-warning"><b>Dogily Farm & Petshop</b></h1>
                    <p style="font-size: 1.25rem" class="text-light" class="ml-14">
                        <strong>Dogily</strong> là thương hiệu đầu tiên tại Việt Nam xây dựng thành công <strong>hệ sinh thái khép kín</strong> gồm các Trang trại nhập khẩu, nhân giống chó mèo cảnh, chuỗi siêu thị thú cưng, Phòng khám thú y, dịch vụ Spa &amp; Grooming tại <strong>Tphcm, Hà Nội &amp; Đà Lạt</strong><br>
                    </p>
                </div>
            </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="container section-title-container" style="margin-bottom:0px;">
    <h2 class="section-title section-title-center">
        <b></b>
        <span class="section-title-main" style="font-size:150%; text-color="light">Giống chó cảnh</span>
        <b></b>
    </h2>
</div>
""", unsafe_allow_html=True)


def img_to_bytes(img_path):
  img_bytes = Path(img_path).read_bytes()
  encoded_img = base64.b64encode(img_bytes).decode()
  return encoded_img

# @st.cache(suppress_st_warning=True)
def write_animals(info, image):
  image_byte = img_to_bytes(image)
  return st.markdown(f"""
          <div class="text-center">
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[3]}&loai={info[2]}' target="_parent">
                <img src='data:image/jpeg;charset=utf-8;base64,{image_byte}' style='height: 100%; width: 100%; object-fit: contain'>
            </a>
            <a href='http://localhost:8501/Chi_Tiết_Sản_Phẩm/?giong={info[3]}&loai={info[2]}' target="_parent">
                <h3 style='text-align: center; color: black; font-size: 30px;'>{info[3]}</h3>
            </a>
          </div>
          """, unsafe_allow_html=True)

df = Data_Shop_CatsnDogs.Data_Shop_CatsnDogs()

list_of_Dogs = df.queryAllDatas("select distinct giong from ShopData where loai='Chó'")

col1, col2 = st.columns(2)
# count = 1
max = 10


with col1:
        for i in range(0,int(len(list_of_Dogs) /2)):
            parent_dir = f"./Chó/{list_of_Dogs[i][0]}"
            image_folder = os.listdir(parent_dir)[0]
            parent_dir += "/" + image_folder
            image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
            image = Image.open(image_path)
            write_animals(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"), image_path)
            st.markdown("----------------------------------")

with col2:
    for i in range(int(len(list_of_Dogs) /2),len(list_of_Dogs)):
        parent_dir = f"./Chó/{list_of_Dogs[i][0]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        image = Image.open(image_path)
        write_animals(df.queryData(f"select * from ShopData where loai='Chó' and giong='{list_of_Dogs[i][0]}'"), image_path)
        st.markdown("----------------------------------")


list_of_Cats = df.queryAllDatas("select distinct giong from ShopData where loai='Mèo'")

st.markdown("""
<div class="container section-title-container" style="margin-bottom:0px;">
    <h2 class="section-title section-title-center">
        <b></b>
        <span class="section-title-main" style="font-size:150%;">Giống Mèo</span>
        <b></b>
    </h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
        for i in range(0,int(len(list_of_Cats) /2)):
            parent_dir = f"./Mèo/{list_of_Cats[i][0]}"
            image_folder = os.listdir(parent_dir)[0]
            parent_dir += "/" + image_folder
            image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
            image = Image.open(image_path)
            write_animals(df.queryData(f"select * from ShopData where loai='Mèo' and giong='{list_of_Cats[i][0]}'"), image_path)
            st.markdown("----------------------------------")

with col2:
    for i in range(int(len(list_of_Cats) /2),len(list_of_Cats)):
        parent_dir = f"./Mèo/{list_of_Cats[i][0]}"
        image_folder = os.listdir(parent_dir)[0]
        parent_dir += "/" + image_folder
        image_path = parent_dir + "/" + os.listdir(parent_dir)[0]
        image = Image.open(image_path)
        write_animals(df.queryData(f"select * from ShopData where loai='Mèo' and giong='{list_of_Cats[i][0]}'"), image_path)
        st.markdown("----------------------------------")

st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)
