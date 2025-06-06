import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { CreateBotComponent } from './create-bot/create-bot.component';
import { BotListComponent } from './bot-list/bot-list.component';
import { BotPageComponent } from './bot-page/bot-page.component';
import { BacktestingComponent } from './backtesting/backtesting.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'bots', component: BotListComponent },
    { path: 'bots/create', component: CreateBotComponent },
    { path: 'bots/:name', component: BotPageComponent },
    { path: 'backtesting', component: BacktestingComponent}
];
