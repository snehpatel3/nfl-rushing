import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { RushingStatistics } from './stats';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost/api'

  constructor(private http: HttpClient) { }

  public getStatsList(queryParams?: HttpParams): Observable<RushingStatistics[]> {
    return this.http.get<RushingStatistics[]>(`${this.API_URL}/list`, {params: queryParams});
  }
}
