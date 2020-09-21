import {Movie} from "./movie";
import {Role} from "./role";

export class Artist {
  constructor(
    public id: number = 0,
    public name: string = '',
    public age: number = 0,
    public gender: string = 'Male',
    public description: string = null,
    public image: string = null,
    public movies: Role[] = null
  ) {}
}
