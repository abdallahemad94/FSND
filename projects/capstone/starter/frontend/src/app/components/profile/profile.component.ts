import { Component, OnInit } from '@angular/core';
import {AuthService} from "@auth0/auth0-angular";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user = {
    nickname: undefined,
    name: undefined,
    picture: undefined,
    email: undefined
  };
  constructor(public auth:AuthService) {
    this.auth.user$.subscribe(res => this.user = res);
  }

  ngOnInit(): void {
  }

}
