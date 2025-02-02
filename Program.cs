using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// MVC yap�land�rmas�
builder.Services.AddControllersWithViews();
builder.Services.AddRazorPages(); // Razor Pages deste�i eklendi

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// G�venli ba�lant� ayarlar�
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// ?? Claude 3 Haiku ve AWS Textract API �a�r�lar�n� desteklemek i�in Controller y�nlendirmesi
app.MapControllers();

// ?? Varsay�lan y�nlendirme (Home Controller'� ve Index action'� varsay�lan olacak)
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
