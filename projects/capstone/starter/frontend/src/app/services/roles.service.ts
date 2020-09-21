import {Inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Role} from "../models/role";

@Injectable({
  providedIn: 'root'
})
export class RolesService {

  constructor(private http: HttpClient, @Inject("API_URL") private readonly ApiUrl: string) { }

  addRole(role: Role){
    this.http.post<any>(`${this.ApiUrl}/roles/new`, role).subscribe();
  }

  deleteRole(roleId: number){
    this.http.delete<any>(`${this.ApiUrl}/roles/${roleId}`).subscribe();
  }
}
