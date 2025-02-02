using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// MVC yapýlandýrmasý
builder.Services.AddControllersWithViews();
builder.Services.AddRazorPages(); // Razor Pages desteði eklendi

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// Güvenli baðlantý ayarlarý
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// ?? Claude 3 Haiku ve AWS Textract API çaðrýlarýný desteklemek için Controller yönlendirmesi
app.MapControllers();

// ?? Varsayýlan yönlendirme (Home Controller'ý ve Index action'ý varsayýlan olacak)
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
