import { Component } from '@angular/core';

@Component({
  selector: 'app-activity-feed',
  imports: [],
  templateUrl: './activity-feed.component.html',
  styleUrl: './activity-feed.component.css'
})
export class ActivityFeedComponent {
  mock_activities = [
    {name: "Test1", message: "Trader Test1 created.", timestamp: "04/21/2025|12:10PM"},
    {name: "Test2", message: "Test2 bought 10 AAPL at 103.30.", timestamp: "04/20/2025|01:12PM"},
    {name: "Test3", message: "Test3 sold 4 NVDA at 104.21.", timestamp: "04/19/2025|09:20AM"},
    {name: "Test1", message: "Trader Test1 created.", timestamp: "04/21/2025|12:10PM"},
    {name: "Test2", message: "Test2 bought 10 AAPL at 103.30.", timestamp: "04/20/2025|01:12PM"},
    {name: "Test3", message: "Test3 sold 4 NVDA at 104.21.", timestamp: "04/19/2025|09:20AM"},
    {name: "Test1", message: "Trader Test1 created.", timestamp: "04/21/2025|12:10PM"},
    {name: "Test2", message: "Test2 bought 10 AAPL at 103.30.", timestamp: "04/20/2025|01:12PM"},
    {name: "Test3", message: "Test3 sold 4 NVDA at 104.21.", timestamp: "04/19/2025|09:20AM"},
    {name: "Test1", message: "Trader Test1 created.", timestamp: "04/21/2025|12:10PM"},
    {name: "Test2", message: "Test2 bought 10 AAPL at 103.30.", timestamp: "04/20/2025|01:12PM"},
    {name: "Test3", message: "Test3 sold 4 NVDA at 104.21.", timestamp: "04/19/2025|09:20AM"},
  ]
}
