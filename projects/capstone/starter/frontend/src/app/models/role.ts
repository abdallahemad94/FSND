export class Role {
  constructor(
    public id: number,
    public artist_id: number,
    public movie_id: number,
    public character: string,
    public artist: string = null,
    public movie: string = null
  ) { }
}
