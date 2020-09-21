import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ArtistsListComponent} from "./components/artists/artists-list/artists-list.component";
import {ArtistViewComponent} from "./components/artists/artist-view/artist-view.component";
import {ArtistFormComponent} from "./components/artists/atrist-form/artist-form.component";
import {MoviesListComponent} from "./components/movies/movies-list/movies-list.component";
import {MovieFormComponent} from "./components/movies/movie-form/movie-form.component";
import {MovieViewComponent} from "./components/movies/movie-view/movie-view.component";
import {ProfileComponent} from "./components/profile/profile.component";

const routes: Routes = [
  {path: "profile", component: ProfileComponent},
  { path: 'artists', children: [
      { path: '', component: ArtistsListComponent},
      { path: 'new', component: ArtistFormComponent },
      { path: 'edit/:id', component: ArtistFormComponent },
      { path: ':id', component: ArtistViewComponent }
    ]},
  { path: 'movies', children: [
      { path: '', component: MoviesListComponent},
      { path: 'new', component: MovieFormComponent },
      { path: 'edit/:id', component: MovieFormComponent },
      { path: ':id', component: MovieViewComponent }
    ]},
  { path: '**', redirectTo: 'movies', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
