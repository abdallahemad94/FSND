import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ArtistsService} from "../../../services/artists.service";
import {Artist} from "../../../models/artist";
import Swal from 'sweetalert2/dist/sweetalert2';
import {RolesService} from "../../../services/roles.service";
import {MoviesService} from "../../../services/movies.service";
import {Role} from "../../../models/role";

@Component({
  selector: 'app-artist-view',
  templateUrl: './artist-view.component.html',
  styleUrls: ['./artist-view.component.css']
})
export class ArtistViewComponent implements OnInit {
  artistId: number;
  artist: Artist = new Artist();
  rolesData;
  constructor(
    private route: ActivatedRoute,
    private artistsService: ArtistsService,
    private router: Router,
    private rolesService: RolesService,
    private  moviesService: MoviesService) {
    this.route.params.subscribe(params => {
      if (params['id'] && !isNaN(params['id']))
        this.artistId = +params['id'];
    });
    this.artistsService.getArtist(this.artistId).subscribe(
      res => this.artist = res.data
    );
  }

  ngOnInit(): void {
    this.moviesService.getNames().subscribe(res => this.rolesData = res.data);
  }

  deleteArtist() {
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
        this.artistsService.deleteArtist(this.artistId);
        this.router.navigate(['/artists']);
      }
    });
  }

  deleteRole(roleId) {
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
        this.rolesService.deleteRole(roleId);
        this.artistsService.getArtist(this.artistId).subscribe(
          res => this.artist = res.data
        );
      }
    });
  }

  async addRole() {
    let data;
    this.moviesService.getNames().subscribe(res => data = res.data);

    let swalHTML = this.getAddRoleForm(this.rolesData);

    const {value: formValue, isConfirmed, isDismissed} = await this.showAddRole(swalHTML);
    if (isConfirmed && !isDismissed && formValue && Object.values(formValue).every(x => x !== '')) {
      let role: Role = new Role(0, this.artistId, +formValue['id'], formValue['character']);
      this.rolesService.addRole(role);
    }
  }

  async showAddRole(swalHTML) {
    return await Swal.fire({
      title: 'Add Role',
      html: swalHTML,
      focusConfirm: false,
      showCancelButton: true,
      confirmButtonText: `Save`,
      preConfirm: () => {
        let id = <HTMLSelectElement>document.getElementById('swal-input1');
        let characterName = <HTMLInputElement>document.getElementById('swal-input2');
        if (id.validity.valid && characterName.validity.valid)
          return {'id': id.value, 'character': characterName.value};
        else return false;
      }
    });
  }

  getAddRoleForm(data) {
    let formHTML = '<h5 class="text-info">Movie</h5>';
    formHTML += '<select id="swal-input1" class="form-control" required>';
    formHTML += `<option value="">Please select a movie</option>`;
    for (let obj of data) {
      formHTML += `<option value="${obj.id}">${obj.name}</option>`;
    }
    formHTML += '</select>';
    formHTML += '<h5 class="text-info">Character</h5>';
    formHTML += '<input id="swal-input2" class="form-control" required>';
    return formHTML;
  }
}
