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
  // Declare state variables
  stats$: Observable<RushingStatistics[]>;
  queryParams = Object();
  dropDown = [
    { val: '', text_val: 'Please select column to sort by'},
    { val: 'yds', text_val: 'Total Rushing Yards (Yds)' },
    { val: 'lng', text_val: 'Longest Rush (Lng)' },
    { val: 'td', text_val: 'Total Rushing Touchdowns (TD)' }
  ];
  isFilterDisabled = true;
  isOptionsCollapsed = false;
  filterValue: string;
  filterOptions = [ {val: 'player', text_val: 'Player Name'} ];

  constructor(private apiService: ApiService, private router: Router, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    // Get any possible query params and make call to api
    this.activatedRoute.queryParams.subscribe(params => {
      for (let key in params) {
        if (key != 'sortBy') {
          this.filterValue = key;
          this.isFilterDisabled = false;
          break;
        }
      }
      let http_params = new HttpParams({fromObject: params});
      this.getStatsList(http_params);
    });
  }

  // Make request to api via the service
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
    // Make call to api 
    this.stats$ = this.apiService.getStatsList(params)
  }

  onSelected(value: string) {
    if (!value) {
      // Do not include query parameters for sorting
      delete this.queryParams.sortBy;

      this.refreshQueryParams();
      return;
    }
    
    // Set column to sort by
    this.queryParams.sortBy = value;

    this.updateQueryParams();
  }

  triggerSearch(value: string) {
    if (value.length < 2) {
      // Do not include query parameters for filtering if user has only keyed in 1 character
      delete this.queryParams[this.filterValue];

      this.refreshQueryParams();
      return;
    }

    // Include query parameters for filtering if user has keyed in at least 2 characters
    this.queryParams[this.filterValue] = value;

    this.updateQueryParams();
  }

  onFilterChange(value: string) {
    if (!value) {
      this.isFilterDisabled = true;
      return;
    }
    // Enable filter input once filter is selected
    this.isFilterDisabled = false;
    this.filterValue = value;
  }

  export() {
    this.buildCsv(this.stats$);
  }

  private buildCsv(data_observable: Observable<RushingStatistics[]>){
    // Subscribe to the current dataset
    data_observable.subscribe((data) => {
      // Build csv for the current dataset
      let csv = "Id,Player Name,Team,Position,Att,Att/G,Yds,Avg,Yds/G,TD,Lng,1st,1st%,20+,40+,FUM\n";
      data.forEach((record) => {
        let values = Object.values(record);
        let line = values.join(',');
        csv += line + '\n';
      });
      // Automatically trigger download
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
