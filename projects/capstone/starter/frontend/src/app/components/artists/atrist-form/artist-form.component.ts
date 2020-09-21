import { Component, OnInit } from '@angular/core';
import {Artist} from "../../../models/artist";
import {ActivatedRoute} from "@angular/router";
import {ArtistsService} from "../../../services/artists.service";

@Component({
  selector: 'app-artist-form',
  templateUrl: './artist-form.component.html',
  styleUrls: ['./artist-form.component.css']
})
export class ArtistFormComponent implements OnInit {
  artist: Artist = new Artist();
  artistId: number;
  constructor(
    private route: ActivatedRoute,
    private artistsService: ArtistsService) {
    this.route.params.subscribe(params => {
      if(params['id'] && !isNaN(params['id']))
        this.artistId = +params['id'];
    });
  }

  ngOnInit(): void {
    if (this.artistId)
      this.artistsService.getArtist(this.artistId).subscribe( res => this.artist = res.data);
  }

  submit() {
    if (this.artistId)
      this.artistsService.editArtist(this.artist);
    else
      this.artistsService.addArtist(this.artist);
  }
}
