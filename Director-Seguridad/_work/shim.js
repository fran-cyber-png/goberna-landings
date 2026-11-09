// Sustituye lo mínimo del JS de Elementor para la vista previa
(function(){
  // fondos con lazy-load de Elementor
  document.querySelectorAll('.e-con').forEach(function(e){ e.classList.add('e-lazyloaded'); });
  // header fijo
  var hd=document.querySelector('.ak-hd'); if(hd){ hd.style.position='sticky'; hd.style.top='0'; hd.style.zIndex='99'; }
  // pestañas anidadas
  document.querySelectorAll('.e-n-tabs').forEach(function(t){
    var titles=t.querySelectorAll(':scope > .e-n-tabs-heading > .e-n-tab-title');
    function show(btn){
      titles.forEach(function(b){
        var on=b===btn; b.setAttribute('aria-selected',on?'true':'false'); b.setAttribute('tabindex',on?'0':'-1');
        var p=document.getElementById(b.getAttribute('aria-controls')); if(p){ p.classList.toggle('e-active',on); p.style.display=on?'':'none'; }
      });
    }
    titles.forEach(function(b){ b.addEventListener('click',function(){ show(b); }); });
    var cur=t.querySelector('.e-n-tab-title[aria-selected="true"]')||titles[0]; if(cur) show(cur);
  });

  // acordeones anidados: misma animación que hace el JS de Elementor (altura del <details>, duración del ajuste
  // n_accordion_animation_duration y un solo ítem abierto si max_items_expended = one)
  document.querySelectorAll('.elementor-widget-n-accordion').forEach(function(w){
    var st={}; try{ st=JSON.parse(w.getAttribute('data-settings')||'{}'); }catch(e){}
    var dur=(st.n_accordion_animation_duration&&+st.n_accordion_animation_duration.size)||400;
    var one=st.max_items_expended!=='multiple';
    var items=[].slice.call(w.querySelectorAll('details.e-n-accordion-item'));
    function anim(d, open){
      var sum=d.querySelector('summary'), from=d.offsetHeight;
      if(d._a){ d._a.cancel(); }
      if(open){ d.open=true; }
      var to=open? d.scrollHeight : sum.offsetHeight;
      d.style.overflow='hidden';
      d._a=d.animate({height:[from+'px', to+'px']},{duration:dur, easing:'cubic-bezier(.4,0,.2,1)'});
      d._a.onfinish=function(){ if(!open) d.open=false; d.style.overflow=''; d._a=null; };
      sum.setAttribute('aria-expanded', open?'true':'false');
    }
    items.forEach(function(d){
      d.querySelector('summary').addEventListener('click', function(ev){
        ev.preventDefault();
        var opening=!d.classList.contains('ak-open');
        if(opening && one){ items.forEach(function(o){ if(o!==d && o.classList.contains('ak-open')){ o.classList.remove('ak-open'); anim(o,false); } }); }
        d.classList.toggle('ak-open', opening);
        anim(d, opening);
      });
      if(d.open) d.classList.add('ak-open');
    });
  });
  // carrusel de docentes (Swiper desde cdnjs)
  function initSwiper(){
    document.querySelectorAll('.elementor-widget-n-carousel .swiper').forEach(function(el){
      var w=el.closest('.elementor-widget-n-carousel');
      var s={}; try{ s=JSON.parse(w.getAttribute('data-settings')||'{}'); }catch(e){}
      // breakpoints como Elementor: al cambiar de ancho sin recargar, el carrusel se recalcula
      var n=function(v,d){ v=+v; return v>0?v:d; };
      var desk=n(s.slides_to_show,3), lap=n(s.slides_to_show_laptop,desk), tab=n(s.slides_to_show_tablet,2), mob=n(s.slides_to_show_mobile,1);
      var gap=s.image_spacing_custom&&s.image_spacing_custom.size!=null?+s.image_spacing_custom.size:20;
      var bp=function(k){ return {slidesPerView:k, slidesPerGroup:k}; };
      new Swiper(el,{slidesPerView:mob,slidesPerGroup:mob,spaceBetween:gap,loop:false,
        breakpoints:{768:bp(tab),1025:bp(lap),1367:bp(desk)},
        navigation:{nextEl:w.querySelector('.elementor-swiper-button-next'),prevEl:w.querySelector('.elementor-swiper-button-prev')},
        pagination:{el:w.querySelector('.swiper-pagination'),clickable:true}});
    });
  }
  if(window.Swiper) initSwiper(); else window.addEventListener('load',function(){ if(window.Swiper) initSwiper(); });
})();
