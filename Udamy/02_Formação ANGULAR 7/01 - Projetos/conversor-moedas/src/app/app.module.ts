import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConversorModule,  } from './conversor';

@NgModule({
  declarations: [
    AppComponent
  ],

  imports: [
    BrowserModule,
    AppRoutingModule,
    ConversorModule,
    FormsModule,
    HttpClientModule
  ],

  providers: [
  ],

  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
