import { Component } from '@angular/core';
import { Navbar } from '../../components/navbar/navbar';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [Navbar, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
}) 
export class Login {}