import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Movie} from "../models/movie";
import {tap} from "rxjs/operators";
import {ToastOptions, ToastyService} from "ng2-toasty";

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  private toastOptions: ToastOptions = new ToastOptions();

  constructor(
    private http: HttpClient,
    @Inject("API_URL") private readonly apiUrl: string,
    private toasty: ToastyService) {
    this.toastOptions.showClose = true;
    this.toastOptions.theme = "bootstrap";
  }

  public getAll(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/movies`);
  }

  public getNames(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/movies/names`);
  }

  public getMovie(movieId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/movies/${movieId}`);
  }

  public deleteMovie(movieId: number): void {
    this.http.delete<any>(`${this.apiUrl}/movies/${movieId}`).pipe(
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

  public addMovie(movie: Movie): void {
    this.http.post<any>(`${this.apiUrl}/movies/new`, movie).pipe(
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

  public editMovie(movie: Movie): void {
    this.http.post<any>(`${this.apiUrl}/movies/edit/${movie.id}`, movie).pipe(
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
