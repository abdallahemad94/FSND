import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ArtistsListComponent} from './components/artists/artists-list/artists-list.component';
import {ArtistsService} from "./services/artists.service";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {NavBarComponent} from './components/nav-bar/nav-bar.component';
import {RouterModule} from "@angular/router";
import {ArtistViewComponent} from './components/artists/artist-view/artist-view.component';
import {ArtistFormComponent} from './components/artists/atrist-form/artist-form.component';
import {FormsModule} from "@angular/forms";
import {MoviesListComponent} from './components/movies/movies-list/movies-list.component';
import {MovieViewComponent} from './components/movies/movie-view/movie-view.component';
import {MovieFormComponent} from './components/movies/movie-form/movie-form.component';
import {MoviesService} from "./services/movies.service";
import {RolesService} from "./services/roles.service";
import {AuthHttpInterceptor, AuthModule, HttpMethod} from "@auth0/auth0-angular";
import { ProfileComponent } from './components/profile/profile.component';
import {ToastyModule} from "ng2-toasty";

@NgModule({
  declarations: [
    AppComponent,
    ArtistsListComponent,
    NavBarComponent,
    ArtistViewComponent,
    ArtistFormComponent,
    MoviesListComponent,
    MovieViewComponent,
    MovieFormComponent,
    ProfileComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule,
    FormsModule,
    ToastyModule.forRoot(),
    AuthModule.forRoot({
      domain: 'casting-agency-proj.us.auth0.com',
      clientId: 'm0uln6ONBopKv589OQkJtYueyquBBDgm',
      audience: 'https://api.casting-agency-proj',
      redirectUri: window.location.origin,
      httpInterceptor: {
        allowedList: [
          {httpMethod: HttpMethod.Post, uri: '*', tokenOptions: {audience: 'https://api.casting-agency-proj'}},
          {httpMethod: HttpMethod.Patch, uri: '*', tokenOptions: {audience: 'https://api.casting-agency-proj'}},
          {httpMethod: HttpMethod.Put, uri: '*', tokenOptions: {audience: 'https://api.casting-agency-proj'}},
          {httpMethod: HttpMethod.Delete, uri: '*', tokenOptions: {audience: 'https://api.casting-agency-proj'}},
        ]
      }
    })
  ],
  providers: [
    ArtistsService,
    MoviesService,
    RolesService,
    {provide: HTTP_INTERCEPTORS, useClass: AuthHttpInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
