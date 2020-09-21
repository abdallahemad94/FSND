import { Component, OnInit } from '@angular/core';
import {ArtistsService} from "../../../services/artists.service";
import {Artist} from "../../../models/artist";
import Swal from 'sweetalert2/dist/sweetalert2';

@Component({
  selector: 'app-artists-list',
  templateUrl: './artists-list.component.html',
  styleUrls: ['./artists-list.component.css']
})
export class ArtistsListComponent implements OnInit {
  artists: Artist[] = [];
  constructor(private artistsService: ArtistsService) { }

  ngOnInit(): void {
    this.artistsService.getAll().subscribe(res => this.artists = res.data);
  }

  deleteArtist(artistId) {
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
        this.artistsService.deleteArtist(artistId);
        this.artistsService.getAll().subscribe(res => this.artists = res.data);
      }
    });
  }
}
