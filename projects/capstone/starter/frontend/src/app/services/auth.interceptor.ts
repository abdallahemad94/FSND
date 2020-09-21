import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AuthService} from "@auth0/auth0-angular";
import {mergeMap} from "rxjs/operators";

class Auth0Client {
}

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private auth: AuthService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    try {
      return this.auth.getAccessTokenSilently({audience: 'https://api.casting-agency-proj'}).pipe(
        mergeMap(
          res => {
            const authReq = request.clone({setHeaders: {Authorization: `bearer ${res}`}});
            return next.handle(authReq);
          }));
    } catch (e) {
      try {
        return this.auth.getAccessTokenWithPopup({audience: 'https://api.casting-agency-proj'}).pipe(
          mergeMap(
            res => {
              const authReq = request.clone({setHeaders: {Authorization: `bearer ${res}`}});
              return next.handle(authReq);
            }));
      } catch (e) {
        return next.handle(request);
      }
    }
  }
}
