import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { ApiService } from '../api.service';
import { RushingStatistics } from '../stats';
import { ThrowStmt } from '@angular/compiler';

@Component({
  selector: 'app-stats-list',
  templateUrl: './stats-list.component.html',
  styleUrls: ['./stats-list.component.css']
})
export class StatsListComponent implements OnInit {
  stats$: Observable<RushingStatistics[]>;
  queryParams = Object();
  dropDown = [
    { val: '', text_val: 'Please select column to sort by'},
    { val: 'yds', text_val: 'Total Rushing Yards (Yds)' },
    { val: 'lng', text_val: 'Longest Rush (Lng)' },
    { val: 'td', text_val: 'Total Rushing Touchdowns (TD)' }
  ];

  constructor(private apiService: ApiService, private router: Router, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(params => {
      let http_params = new HttpParams({fromObject: params});
      this.getStatsList(http_params);
    });
  }

  private getStatsList(params?: HttpParams){
    this.stats$ = this.apiService.getStatsList(params);
  }

  private refreshQueryParams() {
    this.router.navigate(
      ['.'], 
      { relativeTo: this.activatedRoute, queryParams: this.queryParams }
    );
  }
  
  private updateQueryParams(){
    this.router.navigate([],
    {
      relativeTo: this.activatedRoute,
      queryParams: this.queryParams,
      queryParamsHandling: 'merge'
    });
  
    let params = new HttpParams({fromObject: this.queryParams})
    this.stats$ = this.apiService.getStatsList(params)
  }

  onSelected(value: string) {
    if (!value) {
      delete this.queryParams.sortBy;

      this.refreshQueryParams();
      return;
    }

    this.queryParams.sortBy = value;

    this.updateQueryParams();
  }

  triggerSearch(value: string) {
    console.log(value);
    if (value.length < 2) {
      delete this.queryParams.filterBy;

      this.refreshQueryParams();
      return;
    }
    this.queryParams.filterBy = value;

    this.updateQueryParams();
  }

  export() {
    this.buildCsv(this.stats$);
  }

  private buildCsv(data_observable: Observable<RushingStatistics[]>){
    data_observable.subscribe((data) => {
      let csv = "Stat ID,Player Name,Team,Position,Att,Att/G,Yds,Avg,Yds/G,TD,Lng,1st,1st%,20+,40+,FUM\n";
      data.forEach((record) => {
        let values = Object.values(record);
        let line = values.join(',');
        csv += line + '\n';
      });
      this.triggerDownload(csv);
    });
  }

  private triggerDownload(csv_str: string) {
    let blob = new Blob([csv_str], { type: "text/csv" });
    let url = window.URL.createObjectURL(blob);
    let pwa = window.open(url);
    if (!pwa || pwa.closed || typeof pwa.closed == 'undefined') {
        alert( 'Please disable your Pop-up blocker and try again.');
    }
  }

}
