import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ImageResult } from './image-result'

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  url = 'http://localhost:5000/upload'
  constructor(private http: HttpClient) { }
  
  uploadImage(file): Observable<ImageResult[]> {
    // const formData = new FormData();
    // formData.append('file', file);
    // console.log(formData)
    return this.http.post<ImageResult[]>(this.url, file)
  }
}
