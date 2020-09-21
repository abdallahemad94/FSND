import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Artist} from "../models/artist";
import {tap} from "rxjs/operators";
import {ToastOptions, ToastyService} from "ng2-toasty";

@Injectable({
  providedIn: 'root'
})
export class ArtistsService {
  private toastOptions: ToastOptions = new ToastOptions();

  constructor(
    private http: HttpClient,
    @Inject("API_URL") private readonly apiUrl: string,
    private toasty: ToastyService) {
    this.toastOptions.showClose = true;
    this.toastOptions.theme = "bootstrap";
  }

  public getAll(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/artists`);
  }

  public getNames(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/artists/names`);
  }

  public getArtist(artistId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/artists/${artistId}`);
  }

  public deleteArtist(artistId: number): void {
    this.http.delete<any>(`${this.apiUrl}/artists/${artistId}`).pipe(
      tap(next => {
        this.toastOptions.title = "Success";
        this.toastOptions.msg = next.message;
        this.toasty.success(this.toastOptions);
        return next;
      },
        error => {
        this.toastOptions.title = "Failed";
        this.toastOptions.msg = error.error.message || error.message;
        this.toasty.error(this.toastOptions);
        return error;
      })
    ).subscribe();
  }

  public addArtist(artist: Artist): void {
    this.http.post<any>(`${this.apiUrl}/artists/new`, artist).pipe(
      tap(next => {
        this.toastOptions.title = "Success";
        this.toastOptions.msg = next.message;
        this.toasty.success(this.toastOptions);
        return next;
      },
        error => {
        this.toastOptions.title = "Failed";
        this.toastOptions.msg = error.error.message || error.message;
        this.toasty.error(this.toastOptions);
        return error;
      })
    ).subscribe();
  }

  public editArtist(artist: Artist): void {
    this.http.post<any>(`${this.apiUrl}/artists/edit/${artist.id}`, artist).pipe(
      tap(next => {
        this.toastOptions.title = "Success";
        this.toastOptions.msg = next.message;
        this.toasty.success(this.toastOptions);
        return next;
      },
        error => {
        this.toastOptions.title = "Failed";
        this.toastOptions.msg = error.error.message || error.message;
        this.toasty.error(this.toastOptions);
        return error;
      })
    ).subscribe();
  }
}
