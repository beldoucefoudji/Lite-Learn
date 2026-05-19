
import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';
import { Login } from './pages/login/login'; 
export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: Login },
];