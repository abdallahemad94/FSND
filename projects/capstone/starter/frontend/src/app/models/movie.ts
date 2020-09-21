import {Artist} from "./artist";
import {Role} from "./role";

export class Movie {
  constructor(
    public id: number = 0,
    public name: string = '',
    public release_date: Date = new Date(),
    public description: string = null,
    public image: string = null,
    public cast: Role[] = null
  ) {
  }
}
