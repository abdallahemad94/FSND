import { Component, OnInit } from '@angular/core';
import {AuthService} from "@auth0/auth0-angular";

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {
  loggedIn = false;
  user = {
    nickname: undefined,
    picture: undefined
  };
  constructor(public auth: AuthService) {
    auth.isAuthenticated$.subscribe( res =>  this.loggedIn = res);
    auth.user$.subscribe(res => this.user = res);
  }

  ngOnInit(): void {
  }
}
