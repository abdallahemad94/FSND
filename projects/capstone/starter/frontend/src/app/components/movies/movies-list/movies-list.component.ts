import {Component, OnInit} from '@angular/core';
import {MoviesService} from "../../../services/movies.service";
import {Movie} from "../../../models/movie";
import Swal from "sweetalert2/dist/sweetalert2";
import {ToastOptions, ToastyService} from "ng2-toasty";

@Component({
  selector: 'app-movies-list',
  templateUrl: './movies-list.component.html',
  styleUrls: ['./movies-list.component.css']
})
export class MoviesListComponent implements OnInit {
  movies: Movie[] = [];

  constructor(private moviesService: MoviesService, private toasty: ToastyService) {
  }

  ngOnInit(): void {
    this.moviesService.getAll().subscribe(res => {this.movies = res.data});
  }

  deleteMovie(movieId) {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        this.moviesService.deleteMovie(movieId);
        this.moviesService.getAll().subscribe(res => this.movies = res.data);
      }
    });
  }
}
