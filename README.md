# Online-Turkce-Dogal-Dil-Isleme-Yarismasi
Türkiye Açık Kaynak Platformu Doğal Dil İşleme Yarışması için geliştirilmiştir.
Minus 100 Ekibi Türkçe Doğal Dil İşleme Yarışması Projesi

Proje: Sosyal medyada siber zorbalık tespiti ve sosyal medya platformuna bildirimi.

Süreç: Proje süresinin tamamında veri seti oluşturma çalışmaları devam ederken diğer yandan doğal dil işleme, makine öğrenmesi gibi kısımları implement edilecek.
Proje sonunda bir tarayıcı eklentisi oluşturulurken aynı zamanda makine öğrenmesi ve doğal dil işleme topluluğuna siber zorbalıkla ilgili geniş bir veri seti kazandırılmış olacak.

30/07/2020

Projemiz tamamlandı. 11.111 tweetten oluşan bir veri seti oluşturduk. Bu veri seti yaptığımız literatür taramaları sonucu gördüğümüz üzere Türkiye'nin en geniş siber zorbalık veri setidir. Bunu da ülkemizdeki geliştiricilere ve açık kaynak platformuna sunduğumuz önemli bir değer olarak görüyoruz. Veri setindeki tweetler pozitif ve negatif olarak etiketlendi. Veri setimiz 6111 pozitif ve 5000 negatif tweet içeriyor. Veri seti oluştururken kendi yazdığımız scripti ve tweepy kütüphanesini kullandık. Twitter developer hesabımız ile api üzerinden çektiğimiz tweetleri otomatik olarak tagler ve kullanıcı isimlerinden arındırdık daha sonra tek tek okuyarak etiketleme işlemini yaptık.

Projemiz için veri setini oluştururken kullandığımız script de projemizde "Tweet.py" dosyasında yer alıyor. Tweet çekebilmek için gerekli api keyleri hesabımıza özel olduğu için onları silmiş bulunuyoruz bu sebeple o modülü çalıştırmanız ne yazık ki mümkün değil ancak kullanımına demo videomuzda yer vereceğiz.

"Train.py" modülümüz makine öğrenmesi yöntemlerimizi gerçekleştirdiğimiz modül. Bu modülde oluşturduğumuz veri setimizi ön işleme evresinden geçirdikten sonra tfidf vectorizer ile metinlerin sınıflandırılması aşamasına geçiyoruz. Bu aşamada 3 farklı makine öğrenmesi modelini eğitip .sav uzantısı ile kaydediyoruz. Bu 3 model:
LogisticRegression
SGDClassifier
LinearSVC modelleri.
Modellerin eğitimi sırasında k-fold cross validation yöntemi ile veri setimizi 10 parçaya bölerek her bir parça 1 kez test ve 9 kez eğitim ssetinde yer alacak şekilde modelleri eğitiyoruz. Burada shuffle parametresini kullanarak veri setinin rastgele bir şekilde gruplara ayrılmasını sağlıyoruz.

"Test.py" modülümüzü inceleyecek olursak bu modül kendisine gelen tweetleri daha önceden eğitim safhasında kaydedilmiş modellerin her birine göndererek bunların tahminlerini alan ve ensemble yöntemi olan voting ile 3 model arasında en fazla tahmin edilen sonucu döndüren bir yapı mevcut.

"WebApp.py" modülümüz yarışma jürimiz asıl ürünümüzü api keyleri ellerinde olmayacağı için projeyi test edebilmeleri amacıyla hazırlandı. Burada html ve css kullanarak arayüzünü hazırladığımız modülün makine öğrenmesi modellerimizle bağlantısı flask kütüphanesi ile sağlandı. Basit arayüzü ile modelimizin doğruluğunu test etmek için paylaşımı girip enterlamanız yeterli. Aynı zamanda ortaya çıkan sonucu bir sonraki sayfada doğru ya da yanlış olarak değerlendirmenizi istiyoruz. Bu sayede test girdilerimizi de kullanıcı geri bildirimleriyle beraber veri setimize ekliyoruz ve veri setimizi bir sonraki eğitim için genişletiyoruz.

"Block.py" modülümüz ise asıl ilk proje sunumumuzda anlattığımız kısım. Burada modülümüzü çalıştırdığımızda program Twitter hesabımızı dinlemeye başlıyor ve gelen mentionları sürekli inceleyerek siber zorbalık, tehdit, hakaret, beddua içeren mention tespit ettiğinde tweetin sahibini otomatik olarak engelliyor ve tkinter kütüphanesi ile hazırladığımız arayüzümüze tweet sahibi ve tweetin kendisi engellendi ibaresi ile yansıtılıyor. Şu an için 3. kişileri kullanımı için hazır olmayan bu program kişisel api keylerimi gerektirdiği için bu modülü de keyleri silerek yüklüyorum ancak demo videomuzda ve final sunumumuzda programın çalışma şekli sizlerle paylaşılacaktır.
