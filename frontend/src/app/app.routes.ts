import { Routes } from '@angular/router';
import { BodyComponent } from './body/body.component';
import { BotViewerPageComponent } from './bot-viewer-page/bot-viewer-page.component';
import { BotListComponent } from './bot-list/bot-list.component';
import { BotBacktestingComponent } from './bot-backtesting/bot-backtesting.component';

export const routes: Routes = [
    { path: '', component: BodyComponent },
    { path: ':ticker/:trader', component: BotViewerPageComponent},
    { path: 'backtesting', component: BotBacktestingComponent},
    { path: 'bot-list', component: BotListComponent},
];
