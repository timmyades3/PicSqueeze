from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .forms import UploadimageForm, CreategifForm
from .models import Compressedimage, Creategif
import PIL
from PIL import Image
import mimetypes
import os
from django.core.files.storage import default_storage
import imageio
import uuid


class Compress(View):
    def post(self, request):
        form = UploadimageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            quality_u = form.cleaned_data['quality']
            comp_image_u = form.cleaned_data['image']
            comp_image_un = f'{comp_image_u}'

            # compress image
            comp_img = Image.open(comp_image_u)
            comp_image_f = os.path.splitext(comp_image_un)[1]
            comp_save_name = os.path.splitext(
                comp_image_un)[0] + f"_PicSqueeze{comp_image_f}"
            comp_save_path = os.path.join(os.getcwd(), 'media', 'Compressed')
            compressed_image_path = os.path.join(
                comp_save_path, comp_save_name)

            Compressedimage.objects.create(
                compressed_image=compressed_image_path)
            download_link = reverse(
                'download', args=[comp_save_name, comp_save_path])

            if os.path.splitext(comp_image_un)[1] == '.gif' and comp_img.n_frames > 1:
                compressedFrames = []
                compression_level = int(quality_u/10)
                width, height = comp_img.size
                frame_delays = []
                while True:
                    if comp_img.info.get('duration'):
                        frame_delays.append(comp_img.info['duration'])
                    comp_img.seek(comp_img.tell() + 1)
                    break

                duration = sum(frame_delays)
                for i in range(0, comp_img.n_frames):
                    comp_img.seek(i)
                    comp_resized_frame = comp_img.resize(
                        (width, height), resample=Image.LANCZOS)
                    rgba_image = comp_resized_frame.convert("RGBA")
                    compressed_image = rgba_image.convert(
                        "P", dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=256 - compression_level)
                    compressedFrames.append(compressed_image.convert("RGB"))
                compressedFrames[0].save(compressed_image_path, disposal=2, save_all=True,
                                         append_images=compressedFrames[1:], loop=0,
                                         duration=duration, optimize=False, lossless=True)

            else:

                myWidth, myHeight = comp_img.size
                comp_img = comp_img.resize(
                    (myWidth, myHeight), PIL.Image.LANCZOS)
                comp_img.save(compressed_image_path, quality=quality_u)

            # uncompressed image
            initial_image_size = comp_image_u.size
            image_size = initial_image_size
            uncompressed_image_size = self.get_image_size(image_size)

            # compressed image
            final_image = os.path.getsize(compressed_image_path)
            image_size = final_image
            compressed_image_size = self.get_image_size(image_size)

            # context
            context = {
                'form': form,
                'img_f': comp_img,
                'img_u': uncompressed_image_size,
                'im': compressed_image_size,
                'compress_download_link': download_link
            }

            return render(request, 'landing.html', context)

        else:
            image_error = form.errors.get('image')

            context = {
                'img_e': image_error
            }
            return render(request, '404.html', context)

    # get image size
    def get_image_size(self, image_size):
        if image_size >= 1024 and image_size < 1048576:
            image_sn = image_size/1024
            image_snu = round(image_sn, 2)
            image_size = f"{image_snu}KB"
            return image_size
        elif image_size >= 1048576:
            image_sn = image_size/1048576
            image_snu = round(image_sn, 2)
            image_size = f"{image_snu}MB"
            return image_size
        else:
            image_size = f"{image_size}B"
            return image_size

    def get(self, request):
        form = UploadimageForm()

        return render(request, 'landing.html', {'form': form})


class Download(View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def get(self, request, filename, save_path):
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=' + filename
            return response


class Convert(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def post(self, request):
        form = UploadimageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            imageformat_u = form.cleaned_data['imageformat']
            print(imageformat_u)
            conv_image_u = form.cleaned_data['image']
            conv_image_un = f'{conv_image_u}'

            conv_img = Image.open(conv_image_u)
            mywidth, Myheight = conv_img.size
            if conv_img != 'RGB':
                conv_img = conv_img.convert('RGB')

            conv_image_f = imageformat_u
            conv_save_name = os.path.splitext(
                conv_image_un)[0] + f'_PicSqueeze.{conv_image_f}'
            conv_save_path = os.path.join(os.getcwd(), 'media', 'converted')
            converted_image_path = os.path.join(conv_save_path, conv_save_name)
            conv_img.save(converted_image_path)
            download_link = reverse('download', args=[
                                    conv_save_name, conv_save_path])
            context = {
                'form': form,
                'convert_download_link': download_link
            }

            return render(request, 'convert-img.html', context)

        else:
            image_error = form.errors.get('image')

            # context
            context = {
                'img_e': image_error
            }
            return render(request, '404.html', context)

    def get(self, request):
        form = UploadimageForm()

        return render(request, 'convert-img.html', {'form': form})


class Resize(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def post(self, request):
        form = UploadimageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            res_image_width = form.cleaned_data['imagewidth']
            res_image_height = form.cleaned_data['imageheight']
            res_image_u = form.cleaned_data['image']
            res_image_un = f'{res_image_u}'

            res_img = Image.open(res_image_u)
            res_image_f = os.path.splitext(res_image_un)[1]
            res_save_name = os.path.splitext(
                res_image_un)[0] + f'_PicSqueeze{res_image_f}'
            res_save_path = os.path.join(os.getcwd(), 'media', 'resized')
            resized_image_path = os.path.join(res_save_path, res_save_name)

            download_link = reverse(
                'download', args=[res_save_name, res_save_path])

            if os.path.splitext(res_image_un)[1] == '.gif' and res_img.n_frames > 1:
                resizedFrames = []
                frame_delays = []
                while True:
                    if res_img.info.get('duration'):
                        frame_delays.append(res_img.info['duration'])
                    res_img.seek(res_img.tell() + 1)
                    break

                duration = sum(frame_delays)
                for i in range(0, res_img.n_frames):
                    res_img.seek(i)
                    resized_frame = res_img.resize(
                        (res_image_width, res_image_height))
                    rgba_image = resized_frame.convert("RGBA")
                    resizedFrames.append(rgba_image.convert("RGB"))
                resizedFrames[0].save(resized_image_path, disposal=2, save_all=True,
                                      append_images=resizedFrames[1:], loop=0,
                                      duration=duration, optimize=False, lossless=True)

            else:
                res_img = res_img.resize((res_image_width, res_image_height))
                res_img = res_img.convert('RGB')
                res_img.save(resized_image_path)

            context = {
                'form': form,
                'resize_download_link': download_link
            }

            return render(request, 'resize-img.html', context)
        else:
            image_error = form.errors.get('image')

            # context
            context = {
                'img_e': image_error
            }

            return render(request, '404.html', context)

    def get(self, request):
        form = UploadimageForm()

        return render(request, 'resize-img.html', {'form': form})


class Create(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def post(self, request):
        form = CreategifForm(request.POST, request.FILES)
        gif_images = request.FILES.getlist('gif_images')
        if form.is_valid():
            form.save()

            video = form.cleaned_data['video']
            gif_width = form.cleaned_data['gif_width']
            gif_height = form.cleaned_data['gif_height']
            gif_duration = form.cleaned_data['gif_duration']
            gif_name = form.cleaned_data['gif_name']

            if video != None:
                original_filename = video.name
                filename, extension = os.path.splitext(original_filename)
                unique_id = str(uuid.uuid4())[:8]
                modified_filename = f'{filename}_{unique_id}{extension}'
                temp_video_path_f = os.path.join(os.path.join(
                    os.getcwd(), 'media'), 'temp_'+modified_filename)
                temp_video_path = default_storage.save(
                    temp_video_path_f, video)
                c_Format = '.gif'
                c_save_name = filename+'_PicSqueeze'+c_Format
                c_save_path = os.path.join(os.getcwd(), 'media', 'created')
                c_gif_path = os.path.join(c_save_path, c_save_name)
                reader = imageio.get_reader(temp_video_path_f, 'ffmpeg')
                fps = reader.get_meta_data().get('duration')
                writer = imageio.get_writer(
                    c_gif_path, 'GIF', duration=fps, loop=0)
                for frames in reader:
                    writer.append_data(frames)
                reader.close()
                default_storage.delete(temp_video_path)
            else:
                c_Format = '.gif'
                c_save_name = gif_name+'_PicSqueeze'+c_Format
                c_save_path = os.path.join(os.getcwd(), 'media', 'created')
                c_gif_path = os.path.join(c_save_path, c_save_name)
                c_frames = []
                for img in gif_images:
                    Creategif.objects.create(gif_image=img)
                    c_new_frame = Image.open(img)
                    c_new_frame = c_new_frame.resize((gif_width, gif_height))
                    c_frames.append(c_new_frame)
                c_number_of_frames = len(c_frames)
                duration = int(gif_duration*1000/c_number_of_frames)
                c_frames[0].save(c_gif_path,
                                 format='GIF',
                                 append_images=c_frames[1:],
                                 save_all=True,
                                 duration=duration,
                                 loop=0)

            download_link = reverse(
                'download', args=[f'{c_save_name}', c_save_path])

            context = {
                'form': form,
                'c_download_link': download_link
            }

            return render(request, 'creategif.html', context)

        else:
            gif_image_error = form.errors.get('gif_image')
            print(gif_image_error)
            context = {
                'img_e': gif_image_error
            }
            return render(request, '404.html', context)

    def get(self, request):
        form = CreategifForm(request.POST, request.FILES)

        return render(request, 'creategif.html', {'form': form})
