import { Component, OnInit } from '@angular/core';
import {Movie} from "../../../models/movie";
import {ActivatedRoute} from "@angular/router";
import {MoviesService} from "../../../services/movies.service";

@Component({
  selector: 'app-movie-form',
  templateUrl: './movie-form.component.html',
  styleUrls: ['./movie-form.component.css']
})
export class MovieFormComponent implements OnInit {
  movie: Movie = new Movie();
  movieId: number;
  constructor(
    private route: ActivatedRoute,
    private moviesService: MoviesService) {
    this.route.params.subscribe(params => {
      if(params['id'] && !isNaN(params['id']))
        this.movieId = +params['id'];
    });
  }

  ngOnInit(): void {
    if (this.movieId)
      this.moviesService.getMovie(this.movieId).subscribe( res => this.movie = res.data);
  }

  submit() {
    if (this.movieId)
      this.moviesService.editMovie(this.movie);
    else
      this.moviesService.addMovie(this.movie);
  }

  changeDate(event){
    this.movie.release_date = new Date(event);
  }
}
