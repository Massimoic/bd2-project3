import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { UploadService } from './upload.service';
import { ImageResult } from './image-result'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'faces-app';
  imgSrc: string;
  processingImage = false;
  name: string
  images: ImageResult[]
  numResults: string
  method = '0'

  uploadForm = this.fb.group({
    results: new FormControl(null, [Validators.required]),
    file: new FormControl(null, [Validators.required]),
  });

  constructor(private uploadService: UploadService, private fb: FormBuilder) {}

  get uf() {
    return this.uploadForm.controls;
  }

  getImageData(encoded: string) {
    return 'data:image/jpg;base64,' + encoded;
  }

  onImageChange(event) {
    let reader = new FileReader();

    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;
      reader.readAsDataURL(file);

      reader.onload = () => {
        this.imgSrc = reader.result as string
        this.uploadForm.patchValue({
          file: reader.result
        });
      };
    }
  }

  upload() {
    this.processingImage = true;
    this.uploadForm.patchValue({
      results: this.numResults ? this.numResults : '1'
    })
    this.uploadService.uploadImage(this.uploadForm.value).subscribe(
      (res) => {
        this.processingImage = false;
        this.images = res;
        console.log(this.images[0])
      },
      (err) => {
        this.processingImage = false;
        console.log(err);
      })
  }
}
