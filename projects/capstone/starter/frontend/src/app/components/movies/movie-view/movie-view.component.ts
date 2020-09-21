import {Component, OnInit, ViewChild, ViewRef} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {MoviesService} from "../../../services/movies.service";
import {Movie} from "../../../models/movie";
import {RolesService} from "../../../services/roles.service";
import {ArtistsService} from "../../../services/artists.service";
import {Role} from "../../../models/role";
import Swal from 'sweetalert2/dist/sweetalert2';

@Component({
  selector: 'app-movie-view',
  templateUrl: './movie-view.component.html',
  styleUrls: ['./movie-view.component.css']
})
export class MovieViewComponent implements OnInit {
  movieId: number;
  movie: Movie = new Movie();
  rolesData;
  constructor(
    private route: ActivatedRoute,
    private moviesService: MoviesService,
    private artistsService: ArtistsService,
    private rolesService: RolesService,
    private router: Router) {
    this.route.params.subscribe(params => {
      if (params['id'] && !isNaN(params['id']))
        this.movieId = +params['id'];
    });
    this.moviesService.getMovie(this.movieId).subscribe(
      res => this.movie = res.data
    );
  }

  ngOnInit(): void {
    this.artistsService.getNames().subscribe(res => this.rolesData = res.data);
  }

  deleteMovie() {
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
        this.moviesService.deleteMovie(this.movieId);
        this.router.navigate(['/movies']);
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
        this.moviesService.getMovie(this.movieId).subscribe(
          res => this.movie = res.data
        );
      }
    });
  }

  async addRole() {

    let swalHTML = this.getAddRoleForm(this.rolesData);

    const {value: formValue, isConfirmed, isDismissed} = await this.showAddRole(swalHTML);
    if (isConfirmed && !isDismissed && formValue && Object.values(formValue).every(x => x !== '')) {
      let role: Role = new Role(0, +formValue['id'], this.movieId, formValue['character']);
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
    let formHTML = '<h5 class="text-info">Artist</h5>';
    formHTML += '<select id="swal-input1" class="form-control" required>';
    formHTML += `<option value="">Please select an artist</option>`;
    for (let obj of data) {
      formHTML += `<option value="${obj.id}">${obj.name}</option>`;
    }
    formHTML += '</select>';
    formHTML += '<h5 class="text-info">Character</h5>';
    formHTML += '<input id="swal-input2" class="form-control" required>';
    return formHTML;
  }

}
